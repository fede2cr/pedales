# Sodio

## Compresor

## Descripción

Este es el primer pedal diseñado por encargo de un cliente, y existe mucha distancia física entre el taller y el cliente, por lo cual es necesario crear un diseño que sea muy versatil y modular.

De forma similar al famoso compresor LA2, utiliza un panel luminoso (LA2: EL Wire a alto voltaje) para emitir la señal recibida por la guitarra o entrada, y unas fotoceldas para capturar dicha señal.

En nuestro caso vamos a utilizar un [panel de backlight](https://www.adafruit.com/product/1622) y [fotodiodos](https://www.microjpm.com/products/ad35088/) para actualizar el proyecto con componentes modernos, útiles a bajos voltajes.

También se utilizan transistores en algunos casos, y potenciómetros digitales en otros casos, para permitir cambiar entre diferentes versiones del circuito, tratando de eliminar decisiones que debe tomar el ingenierio al diseñar el circuito, que limitan la utilidad del pedal. Por ejemplo algo tan sencillo como los capacitores de entrada, los cuales definen si el pedal es útil para bajo o guitarra, pero limitan instrumentos como guitarras de 7 cuerdas o barítonas.

Para control se piensa usar una Clue para control vía bluetooth. Para esto se va a utilizar un conector [para Microbit](https://www.adafruit.com/product/3888 para control vía bluetooth. Para esto se va a utilizar un conector [para Microbit](https://www.adafruit.com/product/3888).

TODO:
- [x] Prueba básica de circuito
- [ ] Compra de backlight
- [ ] Diseño de PCB
- [ ] Código mínimo para pantalla y control vía bluetooth
