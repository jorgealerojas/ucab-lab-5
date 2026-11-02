# Guía del laboratorio: fronteras y modelos de despliegue

**Unidad:** V — Modelos de despliegue

**Duración:** 1 h 45 min (105 minutos)

**Modalidad:** individual

**Región obligatoria:** US East (Ohio), `us-east-2`

## Reto

Desplegarás dos fronteras de datos en AWS, comprobarás sus controles y aplicarás una política de publicación. Después utilizarás evidencia de arquitectura para distinguir nube pública, privada, híbrida, comunitaria y estrategia multinube.

La pregunta central es:

> ¿Qué evidencia permite afirmar cuál es el modelo de despliegue?

## Reglas de operación

- Usa únicamente `us-east-2`.
- Utiliza exclusivamente los datos ficticios incluidos.
- No desactives Block Public Access.
- No cambies los nombres ni la configuración de los recursos.
- No incluyas credenciales, tokens o URL vigentes en las capturas.
- Elimina el stack completo al finalizar.
- Detente si una salida no coincide con la descripción de la guía.

## Evidencias durante la práctica

Toma las capturas necesarias de cada paso que confirme un resultado. Como mínimo, el informe debe mostrar:

1. Región efectiva y diagnóstico aprobado.
2. Pruebas locales aprobadas.
3. Stack desplegado y nombres de los dos buckets.
4. Inventario con región, cifrado, versionado y Block Public Access.
5. Resultado de la política con registros aceptados y rechazados.
6. Acceso anónimo rechazado.
7. Acceso temporal autorizado, sin revelar una URL todavía vigente.
8. Clasificación de los cinco escenarios.
9. Verificación integral aprobada.
10. Limpieza completada.

Cada captura debe incluir una explicación breve escrita con tus palabras. No captures información ajena al laboratorio.

## 0–8 min — Formular una hipótesis

Antes de utilizar AWS, copia esta tabla en tu informe y marca cada afirmación como verdadera o falsa. No la corrijas todavía.

| Afirmación | Hipótesis inicial |
|---|---|
| Un bucket sin acceso público pertenece a una nube privada. | |
| Dos buckets AWS forman una nube híbrida. | |
| Usar S3 y CloudFormation constituye multinube. | |
| Varias organizaciones usuarias bastan para crear una nube comunitaria. | |
| Una arquitectura puede ser híbrida y multinube al mismo tiempo. | |

Al final volverás a la tabla y justificarás cada corrección.

## 8–20 min — Preparar y validar el entorno

### 1. Abrir CloudShell en Ohio

En la consola AWS, selecciona **US East (Ohio)** y abre CloudShell. La región aparece en la esquina superior derecha.

CloudShell proporciona una terminal autenticada. Abrirlo no crea los buckets del laboratorio.

### 2. Definir la región principal

`export` establece una variable para la sesión actual. Los scripts la consultan antes de permitir cualquier despliegue.

```bash
export AWS_REGION=us-east-2
```

El comando no imprime salida. Si escribiste correctamente el valor, el prompt reaparece de inmediato.

### 3. Definir la región predeterminada

Esta segunda variable evita que una herramienta que consulte `AWS_DEFAULT_REGION` herede otra ubicación.

```bash
export AWS_DEFAULT_REGION=us-east-2
```

El comando tampoco imprime salida. Ambas variables se pierden al cerrar la sesión de CloudShell.

### 4. Comprobar la configuración efectiva

`aws configure list` muestra de dónde obtiene AWS CLI las credenciales y la región. Es una consulta local: no crea ni modifica recursos.

```bash
aws configure list
```

Busca una fila `region` cuyo valor sea `us-east-2` y cuyo origen sea una variable de entorno. No continúes si aparece otra región.

### 5. Descargar el repositorio

`git clone` copia la guía, el código, las pruebas y la plantilla en el almacenamiento de CloudShell. Todavía no crea recursos AWS.

```bash
git clone https://github.com/jorgealerojas/ucab-lab-5.git
```

La salida debe comenzar de forma similar a:

```text
Cloning into 'ucab-lab-5'...
```

Si el directorio ya existe, consulta la sección correspondiente de `TROUBLESHOOTING.md`.

### 6. Entrar en el repositorio

`cd` cambia el directorio activo para que los comandos siguientes encuentren los archivos del laboratorio.

```bash
cd ucab-lab-5
```

Si funciona, no imprime salida. El prompt debe terminar en `ucab-lab-5`.

### 7. Ejecutar las pruebas locales

`make test` comprueba la política de datos, el inventario, los escenarios, la limpieza y la restricción regional. Las pruebas no crean recursos AWS.

```bash
make test
```

La salida enumera las pruebas y debe terminar con `OK`. No despliegues si aparece `FAIL` o `ERROR`.

### 8. Diagnosticar la cuenta

El diagnóstico confirma las herramientas, la región efectiva, la identidad AWS, la sintaxis de CloudFormation y las pruebas locales.

```bash
./scripts/doctor.sh
```

La salida correcta contiene varias líneas que empiezan con `OK` y termina con:

```text
Entorno listo para desplegar en Ohio.
```

El diagnóstico solo consulta la cuenta y valida archivos; no crea buckets.

## 20–32 min — Desplegar la referencia pública

### 9. Crear el stack

El script solicita a CloudFormation los dos buckets S3. También espera hasta que el stack termine y recupera sus nombres.

```bash
./scripts/deploy-lab.sh
```

Durante la ejecución, CloudFormation mostrará mensajes de creación. La salida final debe incluir:

```text
LABORATORIO LISTO
Stack: ucab-lab-5
Bucket de recepción: ucab-lab-5-intake-...
Bucket de aprobados: ucab-lab-5-curated-...
```

Los sufijos dependen de tu cuenta y región. Ambos nombres deben terminar en `us-east-2`.

### 10. Generar el primer inventario

El inventario consulta STS, CloudFormation y las configuraciones de S3. Registra proveedor, región, cifrado, versionado y bloqueo de acceso público.

```bash
./scripts/inspect-aws.sh
```

La salida es un documento JSON. Comprueba que indique:

- `provider`: `aws`.
- `deployment_model`: `publica`.
- `region`: `us-east-2`.
- Dos buckets con `versioning`: `Enabled`.
- Cuatro indicadores de Block Public Access con valor `true`.

El mismo contenido queda guardado en `generated/inventory.json`.

## 32–52 min — Aplicar la frontera de datos

### 11. Examinar los registros de entrada

`python3 -m json.tool` comprueba y presenta el JSON con indentación. Este comando solamente lee el archivo local.

```bash
python3 -m json.tool data/mixed_records.json
```

Debes observar seis registros. Algunos contienen `correo`, `telefono` o un valor no numérico. Esas diferencias permitirán probar la política.

### 12. Ejecutar el experimento

El script realiza cuatro acciones controladas: carga el conjunto original, aplica la política local, carga los registros aprobados y almacena el reporte.

```bash
./scripts/run-experiment.sh
```

La salida describe cada una de las cuatro etapas. Al finalizar debe mostrar:

```text
EXPERIMENTO COMPLETADO
```

El reporte debe indicar seis entradas, tres aceptadas y tres rechazadas. Cada rechazo incluye su razón.

### 13. Revisar el reporte local

Este comando vuelve a mostrar el reporte que produjo la política. No ejecuta nuevamente el experimento ni modifica S3.

```bash
python3 -m json.tool generated/policy_report.json
```

Comprueba que incluya `input_checksum` y `approved_checksum`. Los checksums representan documentos distintos y, por tanto, no deben ser iguales.

### 14. Revisar los datos aprobados

Este comando muestra el archivo que fue cargado en el bucket de aprobados.

```bash
python3 -m json.tool generated/approved_records.json
```

Debe contener únicamente `obs-001`, `obs-003` y `obs-006`. No debe contener información de contacto.

## 52–67 min — Diferenciar acceso y modelo

### 15. Probar una solicitud anónima

El script intenta consultar el objeto aprobado sin firmar la solicitud. Una respuesta HTTP 403 demuestra que el objeto no admite acceso anónimo.

```bash
./scripts/test-anonymous-access.sh
```

La salida correcta es:

```text
RESULTADO ESPERADO: acceso anónimo rechazado con HTTP 403.
El recurso no es público, pero permanece dentro de la nube pública de AWS.
```

Si el script informa que el acceso fue aceptado, detente y no continúes.

### 16. Crear un acceso temporal

Una URL prefirmada autoriza temporalmente una operación concreta sin cambiar la política pública del bucket. El enlace caduca después de 120 segundos.

```bash
./scripts/create-temporary-link.sh
```

La salida contiene una URL larga que comienza con `https://`. Ábrela en otra pestaña y confirma que devuelve los tres registros aprobados.

No captures ni copies la URL al informe mientras siga vigente. Después de dos minutos, una nueva visita debe fallar por expiración.

## 67–84 min — Comparar los modelos

### 17. Analizar los cinco escenarios

El clasificador lee evidencia declarada: organizaciones, infraestructuras, proveedores, integración y gobierno. No consulta AWS ni modifica recursos.

```bash
./scripts/check-scenarios.sh
```

La salida contiene cinco resultados JSON. Cada uno debe mostrar `valid: true`, además de:

| Escenario | Modelo NIST | Multinube |
|---|---|---:|
| Referencia AWS Ohio | pública | no |
| Banco | privada | no |
| Hospital | híbrida | no |
| Consorcio universitario | comunitaria | no |
| Comercio | pública | sí |

Observa que el último caso continúa usando nube pública y, además, adopta una estrategia multinube. El archivo no presenta multinube como un quinto modelo NIST.

### 18. Inspeccionar el escenario híbrido

Este comando presenta el manifiesto del hospital. Solo lee el archivo local.

```bash
python3 -m json.tool scenarios/hibrida.json
```

Identifica las dos infraestructuras, sus modelos componentes y la propiedad `integrated`. Sin integración, la coexistencia de entornos no bastaría para demostrar una solución híbrida.

### 19. Inspeccionar el escenario comunitario

Este comando presenta las organizaciones y condiciones de gobierno del consorcio.

```bash
python3 -m json.tool scenarios/comunitaria.json
```

Busca `common_governance` y `community_exclusive`. Compartir un bucket público sin estas condiciones no convierte la infraestructura en comunitaria.

### 20. Inspeccionar el escenario multinube

Este comando muestra los proveedores del comercio.

```bash
python3 -m json.tool scenarios/multinube.json
```

Verifica que las infraestructuras tengan proveedores diferentes. Dos servicios, buckets o regiones del mismo proveedor no cumplirían esa condición.

## 84–96 min — Consolidar evidencia y decisión

### 21. Generar el resumen técnico

El generador combina el inventario, el reporte de política y los escenarios. Produce un anexo reproducible, pero no redacta las respuestas conceptuales.

```bash
./scripts/generate-evidence.sh
```

La salida debe indicar que se creó `generated/technical-summary.md`.

### 22. Leer el resumen

`sed` muestra las primeras 240 líneas del resumen sin modificarlo.

```bash
sed -n '1,240p' generated/technical-summary.md
```

Comprueba que los conteos, la región y los cinco escenarios coincidan con las evidencias anteriores. Puedes incorporar este archivo como anexo del informe.

### 23. Ejecutar la verificación integral

La verificación consulta el stack, los controles, los objetos, el inventario, los escenarios y las pruebas locales.

```bash
./scripts/verify-lab.sh
```

La salida debe contener varias líneas `OK` y finalizar con:

```text
VERIFICACIÓN INTEGRAL APROBADA
```

No limpies todavía si aparece un error; revisa `TROUBLESHOOTING.md`.

## Preguntas que debes responder

Responde todas las preguntas con tus palabras y conserva la numeración.

1. ¿Por qué los buckets pertenecen a una nube pública aunque tengan bloqueado el acceso público?
2. ¿Cuál es la diferencia entre un recurso privado dentro de AWS y una nube privada?
3. ¿Qué evidencia del inventario permite identificar a AWS como proveedor y a `us-east-2` como región?
4. ¿Qué función cumplen el cifrado, el versionado y Block Public Access? ¿Alguno cambia el modelo de despliegue?
5. ¿Por qué tener dos buckets o varios servicios AWS no constituye multinube?
6. ¿Por qué separar los datos recibidos y aprobados no convierte la arquitectura en híbrida?
7. En el escenario privado, ¿qué control adicional obtiene el banco y qué responsabilidad operativa debe asumir?
8. En el escenario híbrido, ¿qué datos mantendrías en la infraestructura privada y cuáles colocarías en AWS? Justifica la decisión.
9. ¿Qué ocurriría con la solución híbrida si se interrumpe la conexión entre ambos entornos?
10. ¿Qué condiciones de gobierno, acceso y propósito común necesita el consorcio para considerarse una nube comunitaria?
11. ¿Por qué varias universidades con cuentas independientes en AWS no forman automáticamente una nube comunitaria?
12. ¿Por qué utilizar dos proveedores no hace que una aplicación sea automáticamente resiliente?
13. ¿Qué complejidades introduce multinube en identidad, transferencia, observabilidad y operación?
14. Para el consorcio universitario, recomienda una arquitectura. Considera datos y cumplimiento, demanda, capacidad del equipo, economía y dependencia. Indica el beneficio principal, una contrapartida y una alternativa descartada.

Corrige también la tabla de hipótesis inicial y justifica cada cambio.

## 96–105 min — Limpiar la cuenta

### 24. Eliminar todos los recursos

El script recupera exclusivamente los dos buckets del stack `ucab-lab-5`, elimina sus versiones y marcadores, solicita la eliminación del stack y espera su finalización.

```bash
./scripts/cleanup-lab.sh
```

La eliminación de objetos y del stack no se puede deshacer. La salida correcta termina con:

```text
LIMPIEZA COMPLETADA: el stack ya no existe en Ohio.
```

Conserva una captura de esta confirmación.

## Informe a entregar

Entrega un informe individual en un documento de formato libre, como se ha realizado en las prácticas anteriores. Puede ser un documento de texto, una presentación exportada o un PDF, siempre que sea legible y mantenga la secuencia de la práctica.

El informe debe contener:

1. Identificación y fecha.
2. Tabla de hipótesis inicial y tabla corregida.
3. Capturas necesarias de cada paso, con una breve explicación de lo observado.
4. Resultados de la política: aceptados, rechazados y razones.
5. Evidencia de los checksums y del inventario.
6. Evidencia del acceso anónimo rechazado y del acceso temporal, sin revelar una URL vigente.
7. Clasificación de los cinco escenarios.
8. Respuestas numeradas a las catorce preguntas.
9. Decisión arquitectónica final, beneficio, contrapartida y alternativa descartada.
10. Verificación integral aprobada.
11. Confirmación de limpieza.

El resumen generado puede utilizarse como anexo, pero no sustituye las explicaciones, capturas ni respuestas.
