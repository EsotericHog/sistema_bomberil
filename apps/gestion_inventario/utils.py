

def generar_sku_sugerido(producto_global):
    """
    Genera un SKU sugerido basado en un ProductoGlobal.
    Formato: [CATEGORIA]-[MARCA]-[MODELO/ATRIBUTOS]
    """
    
    # 1. Código de Categoría
    # Asumo que tienes un campo 'codigo' en tu modelo Categoria (ej: "EPP")
    try:
        codigo_categoria = producto_global.categoria.codigo
        if not codigo_categoria:
            # Fallback por si el código está vacío
            codigo_categoria = producto_global.categoria.nombre[:3].upper()
    except:
        codigo_categoria = "SIN-CAT"

    # 2. Código de Marca y Atributos
    if producto_global.marca:
        # Es un producto de MARCA
        codigo_marca = producto_global.marca.nombre[:3].upper()
        # Limpia el modelo de espacios y guiones, luego trunca a 6 caracteres
        modelo_limpio = producto_global.modelo.upper().replace(" ", "").replace("-", "")
        codigo_atributos = modelo_limpio[:6] # Usamos 6 caracteres para más claridad
    else:
        # Es un producto GENÉRICO
        codigo_marca = "GEN"
        
        # Lógica para extraer atributos del nombre
        nombre = producto_global.nombre_oficial.upper()
        stop_words = ["DE", "Y", "PARA", "CON", "EL", "LA", "LOS", "LAS", "TALLA", "TRABAJO"]
        
        palabras_clave = [p for p in nombre.split() if p not in stop_words]
        
        # Tomamos las primeras 3 palabras clave (ej: GUANTES, NITRILO, ROJOS)
        atributos_abreviados = []
        for palabra in palabras_clave[:3]:
            if len(palabra) <= 3:
                atributos_abreviados.append(palabra)
            else:
                atributos_abreviados.append(palabra[:3])
        
        codigo_atributos = "-".join(atributos_abreviados)

    # 3. Ensamblar SKU Final
    sku_final = f"{codigo_categoria}-{codigo_marca}-{codigo_atributos}"
    
    # Limpiar por si acaso (ej: "EPP-ROS--")
    sku_final = sku_final.replace('--', '-').strip('-')
    
    return sku_final