class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        #Legge il file CSV e torna una lista di liste con coppie [epoch,temperature].
        time_series = []

        try:
            with open(self.name, 'r') as file:
                next(file)  # Salto l'intestazione

                prev_epoch = None

                for line in file:
                    # Ignoro righe vuote
                    if not line.strip():
                        continue

                    parts = line.split(',')

                    # Verifico se entrambi i valori epoch e temperature sono presenti e non sono vuoti
                    if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
                        try:
                            epoch = int(float(parts[0]))
                            temperature = float(parts[1])

                            #controllo che i timestamp devono essere crescenti e diversi dal timpestamp precendente
                            if prev_epoch is not None and epoch <= prev_epoch:
                                raise ExamException("Errore, i timestamp sono fuori ordine")

                            prev_epoch = epoch
                            time_series.append([epoch, temperature])

                        except ValueError:
                            pass  # Ignora eventuali errori di conversione

        except FileNotFoundError:
            raise ExamException(f"Errore: Non è stato possibile aprire il file.")

        return time_series

def compute_daily_max_difference(time_series):
    #Calcola la massima differenza di temperatura giornaliera dalla lista di liste time_series
    daily_differences = []
    current_day_start = None
    day_temperatures = []

    # Inizializza current_day_start con il primo epoch valido
    if time_series:
        current_day_start = time_series[0][0] - (time_series[0][0] % 86400)

    for epoch, temperature in time_series:
        day_start = epoch - (epoch % 86400)  # Inizio del giorno in formato epoch

        if day_start != current_day_start:
            # Cotrollo se è un nuovo giorno, allora elaboro le temperature del giorno precedente
            if len(day_temperatures) > 1:
                daily_differences.append(round(max(day_temperatures) - min(day_temperatures), 2))
            else:
                daily_differences.append(None)

            # Reimposto le variabili per il nuovo giorno
            current_day_start = day_start
            day_temperatures = [temperature]
        else:
            # Se siamo ancora nello stesso giorno, aggiungo la temperatura alla lista finche non arrivo al nuovo giorno
            day_temperatures.append(temperature)

    # Elabora le temperature dell'ultimo giorno
    if len(day_temperatures) > 1:
        daily_differences.append(round(max(day_temperatures) - min(day_temperatures), 2))

    return daily_differences

# Esempio d'uso
#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#escursione_termica = compute_daily_max_difference(time_series)
#print(escursione_termica)