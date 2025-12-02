import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageEnhance, ImageDraw, ImageOps
import pypdfium2 as pdfium


def crear_mascara_circular(size):
    # Crea una imagen nueva, totalmente transparente (modo 'L' para máscara)
    mask = Image.new('L', size, 0)
    # Crea un objeto para dibujar sobre la máscara
    draw = ImageDraw.Draw(mask)
    # Dibuja un círculo blanco relleno que ocupa toda la imagen
    # El blanco (255) será la parte visible, el negro (0) la transparente
    draw.ellipse((0, 0) + size, fill=255)
    return mask




def generar_preview_documento(documento_instance):
    if not documento_instance.archivo:
        return

    try:
        archivo = documento_instance.archivo
        nombre_archivo = os.path.basename(archivo.name)
        ext = nombre_archivo.split('.')[-1].lower()
        
        imagen_temporal = None

        # --- 1. Obtener imagen base (PDF o Imagen) ---
        if ext == 'pdf':
            file_bytes = archivo.read()
            pdf = pdfium.PdfDocument(file_bytes)
            try:
                page = pdf[0]
                imagen_temporal = page.render(scale=2).to_pil()
            finally:
                pdf.close()
                
        elif ext in ['jpg', 'jpeg', 'png', 'webp']:
            imagen_temporal = Image.open(archivo)

        # --- 2. Procesamiento ---
        if imagen_temporal:
            if imagen_temporal.mode != 'RGBA':
                imagen_temporal = imagen_temporal.convert('RGBA')

            imagen_temporal.thumbnail((800, 800))

            # ============================================================
            # INICIO LÓGICA MARCA DE AGUA REDONDEADA (NIVEL 2+)
            # ============================================================
            estacion = documento_instance.estacion
            
            if estacion and estacion.logo:
                try:
                    watermark = Image.open(estacion.logo).convert("RGBA")

                    # A) Redimensionar logo
                    ancho_objetivo = int(imagen_temporal.width * 0.20)
                    ratio = watermark.height / watermark.width
                    alto_objetivo = int(ancho_objetivo * ratio)
                    watermark = watermark.resize((ancho_objetivo, alto_objetivo), Image.Resampling.LANCZOS)

                    # --- CAMBIO CLAVE: APLICAR MÁSCARA CIRCULAR ---
                    # 1. Creamos una imagen cuadrada del tamaño máximo del logo
                    size = (max(watermark.size), max(watermark.size))
                    # 2. Centramos el logo en ese cuadrado (si no era cuadrado originalmente)
                    watermark_centrado = Image.new('RGBA', size, (255, 255, 255, 0))
                    watermark_centrado.paste(
                        watermark, 
                        ((size[0] - watermark.size[0]) // 2, (size[1] - watermark.size[1]) // 2)
                    )
                    # 3. Creamos la máscara circular y la aplicamos
                    mask = crear_mascara_circular(size)
                    watermark_redondo = ImageOps.fit(watermark_centrado, size, centering=(0.5, 0.5))
                    watermark_redondo.putalpha(mask)
                    # -------------------------------------------

                    # B) Aplicar Transparencia (Opacidad al 40%)
                    alpha = watermark_redondo.split()[3]
                    alpha = ImageEnhance.Brightness(alpha).enhance(0.4) 
                    watermark_redondo.putalpha(alpha)

                    # C) Calcular Posición
                    margen = 20
                    pos_x = imagen_temporal.width - watermark_redondo.width - margen
                    pos_y = imagen_temporal.height - watermark_redondo.height - margen

                    # D) Pegar la marca de agua redondeada
                    imagen_temporal.paste(watermark_redondo, (pos_x, pos_y), watermark_redondo)

                except Exception as e_watermark:
                    print(f"Advertencia: No se pudo aplicar watermark: {e_watermark}")

            # ============================================================
            # FIN LÓGICA MARCA DE AGUA
            # ============================================================

            imagen_temporal = imagen_temporal.convert('RGB')
            thumb_io = BytesIO()
            imagen_temporal.save(thumb_io, format='JPEG', quality=85)
            
            thumb_name = f"preview_{documento_instance.id}.jpg"
            documento_instance.preview_imagen.save(
                thumb_name, 
                ContentFile(thumb_io.getvalue()), 
                save=False
            )
            documento_instance.save(update_fields=['preview_imagen'])

    except Exception as e:
        print(f"Error generando preview: {e}")