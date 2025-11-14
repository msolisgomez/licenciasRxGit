import gradio as gr

def saludo(nombre, edad):
    return "Hola, " + nombre  + ": "+ str(edad) +"Años de edad"

appSuma = gr.Interface(
    fn=saludo,
    inputs=["text", "slider"],
    outputs=["text"],
)

appSuma.launch()