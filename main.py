## Poner filtros para audio y cambiar grafica binarios

import numpy as np
import matplotlib.pyplot as plt
import wave
import os

def plot_audio_signal(audio_path):
    # Abrir el archivo de audio
    audio_file = wave.open(audio_path, 'r')

    # Obtener los parámetros del audio
    sample_width = audio_file.getsampwidth()
    sample_rate = audio_file.getframerate()
    num_frames = audio_file.getnframes()
    duration = num_frames / float(sample_rate)
    num_channels = int(audio_file.getnchannels())
    # Leer los datos de audio
    audio_data = audio_file.readframes(num_frames)

    # Cerrar el archivo de audio
    audio_file.close()

    # Convertir los datos de audio a un array numpy
    audio = np.frombuffer(audio_data, dtype=np.int8)

    # Crear el vector de tiempo
    time = np.linspace(0., duration, num=len(audio))

    # Crear una figura con dos subplots
    fig, ax = plt.subplots(1, 1)

    # Graficar la señal de audio
    ax.plot(time, audio, color='orange')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')

    # Ajustar los márgenes y espaciado
    plt.tight_layout()

    plt.show()

    return [sample_width,sample_rate,num_frames, num_channels]

def to_binary(audio_path):
    # Abrir el archivo de audio
    audio_file = wave.open(audio_path, 'r')

    # Obtener los parámetros del audio
    sample_width = audio_file.getsampwidth()
    sample_rate = audio_file.getframerate()
    num_frames = audio_file.getnframes()
    num_channels = int(audio_file.getnchannels())
    duration = num_frames / float(sample_rate)
    print("sample_width",sample_width)
    print("sample_rate",sample_rate)
    print("num_frames",num_frames)
    print("num_channels", num_channels)
    # Leer los datos de audio
    audio_data = audio_file.readframes(num_frames)

    # Cerrar el archivo de audio
    audio_file.close()

    # Convertir los datos de audio a un array numpy
    audio = np.frombuffer(audio_data, dtype=np.int8)
    audioT = audio

    # Calcular los índices correspondientes al intervalo deseado
    start_index = int(0 * sample_rate)
    end_index = int(0.001 * sample_rate) #Modificar para apreciar de mejor manera el muestreo en binario, el numero que se modifica es el número de segundos a escuchar

    # Recortar la señal de audio al intervalo deseado
    audio = audio[start_index:end_index]

    # Convertir la señal de audio a binario
    binary_signal = np.unpackbits(audio.astype(np.uint8))

    # Mostrar la versión binaria de la señal de audio
    fig, ax = plt.subplots(1, 1)
    ax.plot(binary_signal, 'b.')
    ax.set_xlabel('Muestra')
    ax.set_ylabel('Valor binario')

    # Ajustar los márgenes y espaciado
    plt.tight_layout()
    plt.show()


    #Retornar todo el audio
    return np.unpackbits(audioT.astype(np.uint8))

def encode_rle(binary_audio):
    encoded_audio = []
    count = 1
    for i in range(1, len(binary_audio)):
        if binary_audio[i] == binary_audio[i-1]:
            count += 1
        else:
            encoded_audio.append((binary_audio[i-1], count))
            count = 1
    encoded_audio.append((binary_audio[-1], count))
    return encoded_audio

def decode_rle(encoded_audio):
    decoded_audio = []
    for value, count in encoded_audio:
        decoded_audio.extend([value] * count)
    return np.array(decoded_audio, dtype=np.uint8)

def to_audio(binary_audio, audio_path, info):
    # Convertir la cadena binaria a valores enteros de 8 bits
    binary_audio = binary_audio.astype(np.uint8)

    # Convertir los valores enteros a bytes
    audio_bytes = np.packbits(binary_audio)

    # Abrir un nuevo archivo WAV para escritura
    output_file = wave.open(os.getcwd() + '\\audios\\' + "Generado" + ".wav", 'w')

    # Establecer los parámetros del archivo WAV
    sample_width = info[0]  # 1 byte (8 bits)
    num_channels = info[3]  # Mono
    sample_rate = info[1]  # Tasa de muestreo
    num_frames = info[2]  # Número de frames

    # Establecer los parámetros en el archivo WAV
    output_file.setsampwidth(sample_width)
    output_file.setnchannels(num_channels)
    output_file.setframerate(sample_rate)
    output_file.setnframes(num_frames)

    # Escribir los bytes en el archivo WAV
    output_file.writeframes(audio_bytes)

    # Cerrar el archivo WAV
    output_file.close()

    print("¡Archivo WAV creado exitosamente!")

# Ruta del archivo de audio
nombreCancion = input("Ingrese el nombre del archivo a procesar (sin la extensión): ")
archivo_audio = os.getcwd() + '\\audios\\' + nombreCancion + ".wav"

# Llamar a la función para graficar la señal
info = plot_audio_signal(archivo_audio)

# Llamar a la función para convertir a binario y mostrar la versión binaria
binary_audio = to_binary(archivo_audio)
print("Audio original en binario:")
#print(binary_audio)

# Llamar a la función para realizar la compresión RLE
compressed_audio = encode_rle(binary_audio)
print("Audio comprimido:")
#print(compressed_audio)

# Llamar a la función para realizar la descompresión RLE
decompressed_audio = decode_rle(compressed_audio)

# Verificar si la descompresión es correcta comparando con el audio original
print("¿La descompresión es correcta?", np.array_equal(binary_audio, decompressed_audio))

# Guardar el audio descomprimido en un archivo WAV
to_audio(decompressed_audio, archivo_audio, info)