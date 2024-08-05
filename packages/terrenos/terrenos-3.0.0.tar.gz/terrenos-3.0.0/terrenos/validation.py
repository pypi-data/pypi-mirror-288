from .utils import obtener_seleccionados

def validar_fila(row):
    errors = []
    cambios = []
    if not row[1]:
        errors.append("codigo esta vacio")
    if not row[2]:
        errors.append("primer_nombre_reconocedor esta vacio")
    if not row[3]:
        errors.append("primer_apellido_reconocedor esta vacio")
    if not row[4]:
        errors.append("numero_documento esta vacio")
    if row[5] is None or row[5] == 1:
        row[5] = 0
        cambios.append("tiene_area_registral actualizado a 0")
    if not row[7]:
        errors.append("act_fecha_ esta vacio")
    if not row[8]:
        errors.append("act_destinaciones esta vacio")
    if not row[9]:
        errors.append("procedimiento esta vacio")
    if not row[10]:
        errors.append("resultado_visita esta vacio")
    if row[11] is None:
        errors.append("suscribe_acta_de_colindancia esta vacio")
    if not row[12]:
        errors.append("despojo_o_abandono esta vacio")
    if not row[13]:
        errors.append("estrato esta vacio")
    if not row[14]:
        errors.append("fmi_ esta vacio")
    if not row[15]:
        if row[14]:
            row[15] = row[14]
            cambios.append("folio_ actualizado a fmi_")
        else:
            errors.append("folio_ y fmi_ estan vacios")
    if not row[16] or row[16] != row[1]:
        if row[1]:
            row[16] = row[1]
            cambios.append("npn_ actualizado a codigo")
        else:
            errors.append("npn_ y codigo estan vacios")
    if row[17] is None:
        errors.append("act_novedad_terreno esta vacio")
    else:
        if row[17] == 1 and not row[18]:
            errors.append("novedad_terreno_observ no debe estar vacio cuando act_novedad_terreno es 'Si'")
        elif row[17] == 0 and row[18]:
            errors.append("novedad_terreno_observ debe estar vacio cuando act_novedad_terreno es 'No'")
    return errors, cambios

def validate_attributes(layer):
    where_clause = obtener_seleccionados(layer)
    if (where_clause == "1=0"):
        logging.info("No hay entidades seleccionadas.")
        return

    workspace = arcpy.Describe(layer).path
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()

    try:
        with arcpy.da.UpdateCursor(layer, ["OBJECTID", "codigo", "primer_nombre_reconocedor", "primer_apellido_reconocedor", 
                                           "numero_documento", "tiene_area_registral", "act_area_r", 
                                           "act_fecha_", "act_destinaciones", "procedimiento", 
                                           "resultado_visita", "suscribe_acta_de_colindancia", 
                                           "despojo_o_abandono", "estrato", "fmi_", "folio_", "npn_",
                                           "act_novedad_terreno", "novedad_terreno_observ"], 
                                           where_clause=where_clause) as cursor:
            mensajes = []
            cambios = []
            for row in cursor:
                errores, cambios_fila = validar_fila(row)
                if errores:
                    mensajes.append(f"Errores en el predio {row[1]}:\n" + "\n".join([f"{i+1}. {error}" for i, error in enumerate(errores)]))
                if cambios_fila:
                    cambios.append(f"Predio {row[1]}:\n" + "\n".join([f"{i+1}. {cambio}" for i, cambio in enumerate(cambios_fila)]))
                cursor.updateRow(row)

        if mensajes:
            for mensaje in mensajes:
                logging.error(mensaje)
        else:
            logging.info("Todos los atributos se encuentran debidamente llenos.")

        if cambios:
            logging.info("Cambios realizados en el predio {row[1]}:")
            for cambio in cambios:
                logging.info(cambio)

        decision = input("Validacion completada. ¿Desea confirmar los cambios? (si/no): ").strip().lower()
        if decision == 'si':
            edit.stopOperation()
            edit.stopEditing(True)
            logging.info("Los cambios han sido confirmados.")
        else:
            edit.stopOperation()
            edit.stopEditing(False)
            logging.info("Los cambios han sido abortados.")
    except Exception as e:
        edit.stopOperation()
        edit.stopEditing(False)
        logging.error(f"Ocurrio un error: {e}. Los cambios han sido abortados.")
    finally:
        if edit.isEditing:
            edit.stopEditing(False)