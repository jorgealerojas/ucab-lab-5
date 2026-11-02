# Solución de problemas

## La región efectiva no es Ohio

Los scripts muestran la región detectada y se detienen antes de crear recursos. Confirma que CloudShell esté abierto en US East (Ohio) y vuelve a definir las dos variables indicadas en `LAB_GUIDE.md`.

No edites los scripts para evitar la validación. La cuenta del curso y la plantilla están diseñadas exclusivamente para `us-east-2`.

## El directorio `ucab-lab-5` ya existe

No repitas `git clone` dentro del mismo directorio. Entra en la copia existente y confirma que contiene `LAB_GUIDE.md`, `app`, `infra`, `scripts` y `tests`.

Si la copia pertenece a una ejecución anterior, completa primero la limpieza de cualquier stack que todavía exista.

## `doctor.sh` no puede consultar STS

La sesión de CloudShell puede haber expirado. Recarga CloudShell y confirma que la consola continúa autenticada en la cuenta correcta.

No pegues credenciales manualmente en la terminal ni las incluyas en una captura.

## CloudFormation informa que el bucket ya existe

Los nombres incluyen la cuenta y la región. Este mensaje normalmente indica que un stack anterior o incompleto todavía conserva el bucket.

Abre CloudFormation en Ohio y busca `ucab-lab-5`. Si existe, utiliza el script de limpieza de esta versión del repositorio.

## El stack queda en `ROLLBACK_COMPLETE`

Abre la pestaña **Events** del stack y localiza el primer evento con estado de error. Los eventos posteriores suelen ser consecuencia del primero.

Después de conservar la evidencia del error, ejecuta la limpieza. Corrige la causa antes de volver a desplegar.

## El experimento no encuentra los buckets

Confirma que `deploy-lab.sh` terminó con `LABORATORIO LISTO`. Los scripts recuperan los nombres desde los outputs de CloudFormation y no aceptan nombres escritos manualmente.

## El acceso anónimo no devuelve 403

No continúes. Ejecuta el inventario y confirma que los cuatro indicadores de Block Public Access tengan valor `true`.

No cambies políticas ni ACL para intentar corregirlo. Conserva la salida y limpia el stack si el control no puede verificarse.

## La URL temporal ya expiró

La expiración después de 120 segundos es intencional. Genera una nueva URL si todavía necesitas realizar la comprobación.

No incluyas una URL vigente en el informe.

## `verify-lab.sh` no encuentra un objeto

Vuelve a ejecutar el experimento y comprueba que finalice con `EXPERIMENTO COMPLETADO`. Después repite la verificación integral.

## La eliminación del stack falla

Los buckets versionados deben quedar completamente vacíos. Ejecuta nuevamente `cleanup-lab.sh`; el script puede continuar una limpieza interrumpida.

Si CloudFormation muestra `DELETE_FAILED`, revisa sus eventos en Ohio antes de eliminar recursos manualmente.

## Cerré CloudShell antes de limpiar

Abre una sesión nueva en Ohio, entra al repositorio y vuelve a definir las variables de región. Después ejecuta `cleanup-lab.sh`.

Los archivos locales pueden desaparecer, pero el stack permanece en la cuenta hasta que CloudFormation confirme su eliminación.
