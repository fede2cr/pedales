# TODO para imitator

- [x] test code para mezclar los 4 canales con diferentes volúmen, y posibilidad de cambiar el volumen durante play. Play y pausa.
- [x] test code para descargar audio de youtube, tomar nombre de canción

- [ ] azure function que recibe yt-videoID, extrae el audio, y lo separa con demux, retorna la lista de archivos procesados
- [ ] mangopi con interfaz web, la cual envía yt-videoID, aceptar renorno de lista de 4 archivos y los descarga
- [ ] mangopi con blinka (alpha en raspberry)
- [ ] blinka lee los niveles de volumen para cada canal desde rotary encoders
- [ ] blinka inicia play cuando recibe presión del botón, pausa con otra presión, y reinicio con long press
- [ ] mangopi con interfaz web para buscar videos en youtube
- [ ] mangopi con vpn de zerotier para manejo de actualizaciones de software, OS, etc
- [ ] mangopi con telemetria de cantidad de videos procesados, versiones de software y OS, espacio en disco, temperatura
- [ ] mangopi abre un AP al que uno se pega, le pone los datos de una red wifi que escanee, apaga el AP y se conecta como SU a esa red wifi
- [ ] mangopi al prender la mae, si no encuentra la red wifi, parpadea los leds y activa el AP de nuevo para configurarle la nueva red
- [ ] mangopi se publica por mDNS
