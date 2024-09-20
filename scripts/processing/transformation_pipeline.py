import transformation_functions as tf
import pandas as pd


def transformation_pipeline(df):
    df = df.pipe(tf.normalizar_nombres_columnas)


    return (df
        .pipe(tf.estandarizar_marcas)
        .pipe(tf.extraer_marcas)
        .pipe(tf.extraer_anios)
        .pipe(tf.extraer_modelos)
        .pipe(tf.remover_textos)
        .pipe(tf.transformar_sport_edition)
        .pipe(tf.estandarizar_modelos)
        .pipe(tf.transformar_precios)
    )



