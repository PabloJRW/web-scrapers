import transformation_functions as tf
import pandas as pd


def transformation_pipeline(df):
    if df is None:
        raise ValueError("El DataFrame inicial es None.")

    return (df
        .pipe(tf.estandarizar_marcas)
        .pipe(tf.extraer_marcas)
        .pipe(tf.extraer_anios)
        .pipe(tf.extraer_modelos)
        .pipe(tf.remover_textos)
        .pipe(tf.transformar_sport_edition)
        .pipe(tf.estandarizar_modelos)
        .pipe(tf.normalizar_valores_columnas)
        .pipe(tf.transformar_anio)
        .pipe(tf.transformar_precios)
        .pipe(tf.selector_columnas)
    )

