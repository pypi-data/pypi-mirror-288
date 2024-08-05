def obtener_capa_activa(index):
    mxd = arcpy.mp.ArcGISProject("CURRENT")
    mapa_activo = mxd.activeMap
    capa_activa = mapa_activo.listLayers()[index]
    nombre_capa = capa_activa.name
    logging.info(f"Trabajando en la capa: {nombre_capa}")
    return capa_activa

def obtener_seleccionados(capa):
    selection_set = capa.getSelectionSet()
    if not selection_set:
        return "1=0"
    
    oid_field_name = arcpy.Describe(capa).OIDFieldName
    sql_expression = f"{oid_field_name} IN ({','.join(map(str, selection_set))})"
    return sql_expression