# Data Interview Gym --- Product Roadmap & Vision

> **Documento vivo.** Cada decisión de producto, contenido, diseño o
> código debe justificarse contra este documento. Si una feature no
> mejora el aprendizaje, la retención o la preparación para entrevistas,
> no se construye.

------------------------------------------------------------------------

# 1. Tesis del producto

La meta es construir la forma más rápida y práctica para que alguien se
prepare para una entrevista de Data mediante sesiones cortas y
frecuentes.

El problema no es la falta de preguntas.

Los candidatos suelen:

-   guardar cientos de preguntas;
-   leer respuestas de forma pasiva;
-   olvidar lo estudiado;
-   practicar temas al azar;
-   no saber cuáles son sus debilidades;
-   descubrir sus fallas recién durante la entrevista.

## Enfoque

> **Don't study interviews. Practice them.**

La experiencia debe sentirse más como:

**Duolingo + examen teórico de conducir + simulador de entrevistas**

y no como:

-   un curso;
-   un repositorio de preguntas;
-   un simple chatbot.

## Promesa

> **Easy to start. Fast to practice. Hard to forget.**

------------------------------------------------------------------------

# 2. North Star Metric

La métrica principal no debe ser registros ni cantidad de preguntas
creadas.

## OMTM

> **% de usuarios nuevos que completan al menos 3 sesiones en sus
> primeros 7 días, incluyendo al menos una sesión de "Practice My
> Mistakes".**

Esto mide que el usuario haya experimentado el loop principal del
producto.

## Health metrics

### Activación

\% de usuarios que completan el diagnóstico inicial.

### Learning Loop

\% de usuarios que vuelven específicamente para practicar errores.

### Retención

Usuarios que regresan en:

-   Día 1
-   Día 7
-   Día 30

### Learning outcome

\% de usuarios que mejoran su rendimiento en sus áreas débiles después
de sesiones de revisión.

### Aha moment

Momento en que el usuario recibe feedback, entiende por qué falló y
logra resolver una nueva pregunta sobre el mismo concepto.

------------------------------------------------------------------------

# 3. Alcance inicial

## V1 --- Data Engineer

No lanzar inicialmente con múltiples roles.

El primer producto será exclusivamente:

> **Data Engineer Interview Prep**

El modelo de datos debe ser suficientemente flexible para soportar
posteriormente:

-   Data Analyst
-   Analytics Engineer
-   ML Engineer
-   Data Scientist

Pero no construir esos tracks hasta validar el primero.

## Expansión

``` text
V1  Data Engineer
 ↓
V2  Data Analyst
 ↓
V3  Analytics Engineer
 ↓
V4  ML Engineer
 ↓
V5  Data Scientist
```

------------------------------------------------------------------------

# 4. User Journey

## Primer ingreso

El usuario selecciona:

### Role

> Data Engineer

### Goal

-   First interview
-   Interview in \<30 days
-   Interview in 1--3 months
-   General practice

Después:

> **Take the 5-question diagnostic**

El diagnóstico establece una línea base.

Ejemplo:

``` text
SQL              4/5
Python           3/5
ETL / ELT        2/5
Data Modeling    2/5
Cloud            1/5
System Design    1/5
```

La aplicación no debe simplemente mostrar resultados.

Debe decir:

> **Your biggest opportunity: System Design**

CTA:

> **Practice my weak areas**

------------------------------------------------------------------------

# 5. Home Screen

La pantalla principal debe responder una sola pregunta:

> **What should I practice right now?**

Ejemplo:

``` text
Good morning 👋

Today's practice
8 questions · ~6 min

[ START ]

You should review:
⚠ System Design
⚠ GCP

3 questions are due for review.

[ PRACTICE MY MISTAKES ]

Readiness
███████░░░ 72%
```

Evitar una pantalla llena de métricas.

El usuario debe saber inmediatamente cuál es la próxima acción.

------------------------------------------------------------------------

# 6. Core Learning Loop

El núcleo del producto es:

``` text
Practice
   ↓
Immediate feedback
   ↓
Identify mistakes
   ↓
Understand the concept
   ↓
Repeat at the right time
   ↓
Increase difficulty
   ↓
Simulate interview
   ↓
Measure readiness
```

El valor diferencial no está en tener más preguntas que otros sitios.

Está en combinar:

> **High-quality content + adaptive practice + mistake repetition**

------------------------------------------------------------------------

# 7. Progresión de aprendizaje

La plataforma debe llevar al usuario por cuatro niveles.

## 1. RECOGNIZE

Multiple choice.

> ¿Reconozco la respuesta correcta?

## 2. RECALL

Flashcards / short answer.

> ¿Puedo recordarla sin ver opciones?

## 3. EXPLAIN

Interview answer.

> ¿Puedo explicarlo claramente?

## 4. APPLY

Scenario / system design.

> ¿Puedo usar el concepto en una situación real?

``` text
Recognize
   ↓
Recall
   ↓
Explain
   ↓
Apply
```

Conocer la respuesta correcta en multiple choice no significa estar
preparado para una entrevista.

------------------------------------------------------------------------

# 8. Practice Modes

## 8.1 Multiple Choice

Modo principal para aprender.

Ejemplo:

> A dashboard only needs to update once per day. Which approach would
> you normally choose?

A. Streaming\
B. Batch\
C. Real-time CDC\
D. Event sourcing

Resultado:

``` text
✓ Correct

B — Batch
```

Mostrar:

### Why

Explicación corta.

### Why not the others

Una razón breve para cada distractor.

### Interview tip

Una recomendación práctica.

------------------------------------------------------------------------

# 9. Question Quality Standard

Cada pregunta debe:

-   tener una única mejor respuesta;
-   tener distractores plausibles;
-   explicar por qué los distractores son incorrectos;
-   probar un concepto relevante;
-   tener dificultad definida;
-   tener un objetivo de aprendizaje;
-   evitar trivia innecesaria;
-   evitar preguntas diseñadas solamente para confundir.

## Mal ejemplo

> Which service has exactly X internal implementation detail?

## Buen ejemplo

> You need to replicate PostgreSQL changes to a cloud warehouse with low
> latency. Which approach is most appropriate?

La prioridad es evaluar:

**reasoning \> memorization**

------------------------------------------------------------------------

# 10. Flashcards

Ejemplo:

> **What is idempotency?**

Botón:

> **Show answer**

Respuesta:

> An operation is idempotent when executing it multiple times produces
> the same final result.

Después:

-   Again
-   Hard
-   Good
-   Easy

La aplicación decide cuándo volver a mostrar la tarjeta.

El usuario no debería tener que administrar manualmente sus decks.

------------------------------------------------------------------------

# 11. Short Answer

Ejemplo:

> Explain OLTP vs OLAP in your own words.

La evaluación debe buscar conceptos clave y no coincidencia textual.

Ejemplo de conceptos esperados:

``` text
OLTP
→ operational / transactional workloads
→ frequent inserts / updates

OLAP
→ analytical workloads
→ aggregations / historical analysis

Warehouse
→ analytical workloads
```

Una respuesta no necesita reproducir exactamente el answer key.

------------------------------------------------------------------------

# 12. Interview Mode

El usuario recibe una pregunta abierta y responde como si estuviera
frente a un entrevistador.

Ejemplos:

-   Design a data pipeline.
-   Explain ETL vs ELT.
-   How would you handle duplicates?
-   How would you ensure data quality?
-   Batch vs streaming?
-   How would you migrate PostgreSQL to BigQuery?

Evaluar:

-   Technical coverage
-   Structure
-   Missing concepts
-   Trade-offs
-   Clarity

------------------------------------------------------------------------

# 13. Interview Answer Framework

Para preguntas abiertas se enseña una estructura repetible:

``` text
1. Direct answer
2. 3–5 technical points
3. Trade-off
4. Connection to experience
```

Esta estructura está presente en el material de preparación original.

La app debe convertirla en una herramienta de entrenamiento.

## Progressive hints

### Hint 1

> Start with the direct answer.

### Hint 2

> Mention the main technical considerations.

### Hint 3

> What is the trade-off?

### Hint 4

> Can you connect this to something you have actually worked on?

El objetivo es aprender a **estructurar una respuesta**, no memorizar un
párrafo.

------------------------------------------------------------------------

# 14. Trade-offs

Los trade-offs deben ser una habilidad de primera clase.

La estructura:

``` text
Decision
   ↓
What did I gain?
   ↓
What did I lose?
   ↓
Why was it acceptable?
```

## Ejemplo --- ELT vs ETL

Una respuesta sólida puede explicar:

-   por qué se eligió ELT;
-   qué flexibilidad aporta;
-   qué complejidad adicional de governance introduce;
-   por qué esa complejidad es aceptable.

## Ejemplo --- Batch vs Streaming

Una respuesta sólida puede explicar:

-   batch cuando no se necesita tiempo real;
-   streaming cuando la latencia importa;
-   el trade-off de complejidad, costo y operación.

La app debe enseñar al usuario a responder:

> **"Why did you choose this?"**

y no solamente:

> **"What is this?"**

------------------------------------------------------------------------

# 15. Killer Feature --- Practice My Mistakes

Debe ser una de las dos CTAs principales.

El sistema registra:

-   respuestas incorrectas;
-   errores repetidos;
-   conceptos débiles;
-   tiempo de respuesta;
-   dificultad percibida;
-   tarjetas olvidadas.

Después genera una sesión personalizada.

> **Practice my mistakes**

## Importante: no repetir mecánicamente

Si el usuario falla varias veces:

``` text
Original question
      ↓
Simpler explanation
      ↓
New question testing same concept
      ↓
Different scenario
      ↓
Original question again
```

Así se comprueba que aprendió el concepto y no que memorizó:

> "La respuesta era B."

------------------------------------------------------------------------

# 16. Weakness Engine

No definir debilidad solamente como porcentaje de aciertos.

Considerar:

-   accuracy;
-   recency;
-   difficulty;
-   number of attempts;
-   repeated failures;
-   response time;
-   confidence.

Mostrar categorías comprensibles:

``` text
Strong
Good
Needs Practice
Priority
```

Ejemplo:

``` text
SQL              Strong
ETL / ELT         Good
Data Modeling     Needs Practice
System Design     Priority
```

Y siempre recomendar una acción.

> **Recommended next session: System Design**

------------------------------------------------------------------------

# 17. Spaced Repetition

Cada pregunta/concepto debe tener un estado:

``` text
New
 ↓
Learning
 ↓
Known
 ↓
Mastered
```

Los errores hacen que el contenido vuelva antes.

Los aciertos consistentes aumentan el intervalo.

El algoritmo puede evolucionar con el tiempo, pero la UX debe mantenerse
simple:

> **12 reviews due today**

------------------------------------------------------------------------

# 18. Readiness Score

Mostrar un score general:

> **Interview readiness: 72%**

Pero nunca presentarlo como:

> "72% probability of getting hired."

Es una métrica interna de preparación.

Ejemplo:

``` text
SQL              87
Python            71
ETL / ELT         78
Data Modeling     61
Cloud             68
System Design     52
Behavioral        81
```

El objetivo es responder:

> **Where should I improve next?**

------------------------------------------------------------------------

# 19. Curriculum --- Data Engineer

El curriculum se organiza por competencias, no por empresas.

## SQL

-   Fundamentals
-   Joins
-   Aggregations
-   Window functions
-   CTEs
-   Interview problems

## Python

-   Fundamentals
-   Data manipulation
-   Scripting
-   Problem solving

## Data Pipelines

-   ETL / ELT
-   Batch
-   Streaming
-   Incremental loads
-   Idempotency
-   Backfills
-   Schema changes

## Data Modeling

-   OLTP vs OLAP
-   Normalization
-   Denormalization
-   Star schema
-   Snowflake schema
-   Fact tables
-   Dimension tables
-   SCD
-   Keys

## Data Quality

-   Nulls
-   Duplicates
-   Referential integrity
-   Row counts
-   Freshness
-   Schema validation
-   Business validation

## Cloud

Inicialmente priorizar GCP:

-   BigQuery
-   Cloud SQL
-   Cloud Composer
-   Dataflow
-   Dataproc
-   GCS
-   Pub/Sub
-   Datastream
-   Partitioning
-   Clustering

Posteriormente:

-   AWS
-   Azure

## dbt

-   Models
-   `source()`
-   `ref()`
-   Tests
-   Macros
-   Incremental models
-   Lineage
-   Dependencies
-   Documentation

## Architecture / System Design

-   Pipeline design
-   Source selection
-   Batch vs streaming
-   Storage
-   Transformation
-   Orchestration
-   Monitoring
-   Alerting
-   Access control
-   Backfills
-   Trade-offs

## Behavioral

-   Ambiguity
-   Leadership
-   Stakeholder disagreement
-   Process improvement
-   Mistakes
-   Complex technical projects

------------------------------------------------------------------------

# 20. Content Architecture

Las preguntas no deben existir como objetos aislados.

``` text
Question
  ↓
Concept
  ↓
Skill
  ↓
Category
  ↓
Role
```

Ejemplo:

``` text
Question:
"When would you choose batch over streaming?"

Concepts:
- Batch
- Streaming
- Latency
- Cost
- Complexity

Skill:
Architecture trade-offs

Category:
Data Pipelines

Role:
Data Engineer
```

Esto permite generar sesiones dirigidas por debilidades.

------------------------------------------------------------------------

# 21. Question Types

El sistema debe soportar:

``` text
multiple_choice
flashcard
short_answer
scenario
system_design
behavioral
trade_off
sql_problem
```

Cada pregunta también puede tener:

``` text
difficulty:
easy
medium
hard
expert
```

Y:

``` text
skill:
recognition
recall
explanation
application
```

------------------------------------------------------------------------

# 22. Question Schema

Cada pregunta debe poder almacenar:

``` text
id
role
category
subcategory
difficulty
question_type
skill_level

question

options[]
correct_answer

explanation
wrong_answer_explanations[]

key_concepts[]
common_mistake
interview_tip

answer_framework
ideal_answer

expected_concepts[]
must_mention[]
nice_to_mention[]
trade_off[]

related_question_ids[]

source
```

La estructura debe permitir que una misma pregunta se conecte con otras
preguntas que evalúan el mismo concepto.

------------------------------------------------------------------------

# 23. Content Creation Pipeline

Las notas originales de entrevistas son **source material**, no
contenido público final.

Pipeline:

``` text
Raw interview notes
        ↓
Extract concepts
        ↓
Separate generic knowledge from personal experience
        ↓
Generalize company-specific context
        ↓
Create interview question
        ↓
Create distractors
        ↓
Create explanation
        ↓
Add common mistakes
        ↓
Add interview tip
        ↓
Assign difficulty
        ↓
Assign skill
        ↓
Human review
        ↓
Question bank
```

La meta es preservar la calidad y el realismo de las notas sin convertir
el producto en una colección de respuestas personales o preguntas
filtradas de empresas.

------------------------------------------------------------------------

# 24. Initial Question Bank

## Phase 1

**50 high-quality questions**

Suggested distribution:

``` text
SQL                 10
Data Pipelines       8
ETL / ELT            6
Data Modeling        6
Data Quality         5
Cloud                6
dbt                  4
Architecture         3
Behavioral           2
```

## Phase 2

Expand to:

**100--150 questions**

La regla es:

> **Quality \> quantity**

------------------------------------------------------------------------

# 25. Daily Practice

Sesiones de:

> **5--10 minutes**

Ejemplo:

``` text
2 new questions
3 review questions
2 mistakes
1 challenge question
```

El usuario no debería tener que decidir qué estudiar.

La aplicación decide.

------------------------------------------------------------------------

# 26. Mock Interview

Una vez validado el learning loop:

``` text
DATA ENGINEER MOCK INTERVIEW

10 questions
20 minutes

SQL              2
Pipelines        2
Modeling         2
Cloud             1
Architecture      1
System Design     1
Behavioral        1
```

Resultado:

``` text
Practice score: 76%

Strong:
✓ SQL
✓ ETL

Needs work:
⚠ Cloud
⚠ System Design

Recommended next session:
System Design — 10 questions
```

------------------------------------------------------------------------

# 27. Gamification

Mantenerla ligera.

## Sí

-   Daily streak
-   Questions completed
-   Topics mastered
-   Readiness score
-   Weekly goal

## No

-   puntos sin significado;
-   exceso de badges;
-   leaderboards artificiales;
-   gamificación que distraiga del aprendizaje.

La recompensa principal debe ser:

> **I am getting better at interviews.**

------------------------------------------------------------------------

# 28. LinkedIn Growth Strategy

No lanzar la app con un simple:

> "I built an app."

Primero construir audiencia alrededor del problema.

------------------------------------------------------------------------

## Phase 1 --- Roadmap Post

Carrusel:

> **How I would prepare for a Data Engineering interview**

Mostrar:

``` text
SQL
↓
Python
↓
Pipelines
↓
ETL / ELT
↓
Data Modeling
↓
Data Quality
↓
Cloud
↓
Architecture
↓
System Design
↓
Behavioral
```

CTA:

> **Which one would you struggle with most?**

------------------------------------------------------------------------

# 29. Weekly Interview Series

Después del roadmap:

## Week 1 --- SQL

> **Data Engineering Interview Question #1**

Mostrar pregunta + A/B/C/D.

CTA:

> **What's your answer?**

No revelar inmediatamente.

Luego publicar:

> **Answer: B**

con explicación.

Repetir con:

-   ETL / ELT
-   Data Modeling
-   Data Quality
-   Cloud
-   dbt
-   System Design
-   Behavioral

------------------------------------------------------------------------

# 30. Content Repurposing

Una pregunta puede convertirse en varios contenidos:

``` text
Question
 ↓
LinkedIn quiz
 ↓
Comments
 ↓
Answer post
 ↓
Explanation
 ↓
Carousel
 ↓
App question
```

Esto permite producir contenido de manera eficiente.

------------------------------------------------------------------------

# 31. Product Funnel

``` text
LinkedIn post
      ↓
Free question
      ↓
Website
      ↓
5-question diagnostic
      ↓
Personalized weak areas
      ↓
Daily practice
      ↓
Habit
      ↓
Mock interview
```

El contenido de LinkedIn funciona como top of funnel del producto.

------------------------------------------------------------------------

# 32. Product Launch

Después de publicar suficientes preguntas:

> I've been sharing Data Engineering interview questions here for the
> past few weeks.

> I turned them into a free practice tool.

> You can now practice questions, repeat your mistakes and track your
> weak areas.

CTA:

> **Practice Data Engineering interviews**

La audiencia ya debe haber experimentado el problema antes de ver el
producto.

------------------------------------------------------------------------

# 33. Monetization

La monetización debe tratarse inicialmente como una **hipótesis**, no
como una arquitectura definitiva.

## Posible modelo

### Free

-   Diagnóstico
-   Multiple choice
-   Flashcards
-   Práctica básica
-   Cantidad limitada de feedback avanzado

### Pro

-   Evaluaciones avanzadas
-   Interview mode
-   Mock interviews
-   Trade-off analysis
-   Personalización más profunda

### Principio

No bloquear la experiencia básica.

El usuario debe poder entender el valor antes de pagar.

La limitación de features de IA puede funcionar como paywall, pero debe
validarse con usuarios reales.

No introducir un sistema complejo de "AI tokens" hasta comprobar que
existe consumo significativo y que el costo de IA requiere esa
restricción.

------------------------------------------------------------------------

# 34. Technical Architecture --- Only When Needed

La arquitectura debe ser suficiente para validar el producto.

## Principio

> **Do not build infrastructure for users you don't have yet.**

El MVP no necesita:

-   Snowflake para telemetría;
-   Redis/BullMQ por defecto;
-   arquitectura enterprise;
-   mobile offline-first;
-   múltiples clouds;
-   microservicios innecesarios.

Primero validar:

``` text
Question
→ Answer
→ Feedback
→ Mistake
→ Review
```

Después escalar los componentes que realmente se conviertan en
bottlenecks.

## Seguridad

La privacidad y separación de datos de usuarios sí es obligatoria desde
el inicio, pero debe implementarse con la solución más simple que cumpla
el requisito.

------------------------------------------------------------------------

# 35. AI Strategy

La IA es un acelerador, no el producto.

## Usos principales

-   evaluar respuestas abiertas;
-   explicar errores;
-   generar variantes de una pregunta;
-   detectar conceptos faltantes;
-   dar feedback de entrevistas;
-   personalizar práctica.

## Principio

> **The core learning loop must work without requiring an expensive LLM
> call for every click.**

Multiple choice y gran parte del feedback pueden ser determinísticos.

La IA debe aparecer donde realmente agrega valor.

------------------------------------------------------------------------

# 36. MVP

## P0 --- Must Have

-   Data Engineer role
-   50 high-quality questions
-   Multiple choice
-   Explanations
-   Plausible distractors
-   Categories
-   Difficulty
-   Initial diagnostic
-   Mistake tracking
-   Practice My Mistakes
-   Basic spaced repetition
-   Basic progress dashboard

## P1 --- Consolidation

-   Flashcards
-   Short answers
-   Readiness score
-   Interview answer framework
-   Trade-off mode
-   Daily practice
-   100--150 questions
-   Mock interview

## P2 --- Expansion

-   AI answer evaluation
-   Voice interview
-   Personalized interview simulation
-   Company-specific tracks
-   Data Analyst
-   Analytics Engineer
-   ML Engineer
-   Data Scientist

## P3 --- Only after validation

-   Mobile app
-   Offline practice
-   Push notifications
-   Advanced infrastructure
-   Additional clouds
-   Advanced monetization

------------------------------------------------------------------------

# 37. Anti-Roadmap

No vamos a construir:

## Un curso

Cero lecciones gigantes.

## Un basurero de preguntas

500 preguntas aleatorias no hacen un producto.

## Un simple AI wrapper

La IA puede evaluar y personalizar, pero el learning loop debe existir
sin depender completamente de ella.

## Una plataforma de certificación

Esto prepara para entrevistas.

No otorga certificaciones profesionales.

## Una base de datos de filtraciones

Usar preguntas originales y escenarios realistas.

No construir el producto alrededor de preguntas robadas o propietarias.

------------------------------------------------------------------------

# 38. Success Criteria

Antes de expandir el producto, demostrar:

### 1. Activation

Los usuarios completan el diagnóstico.

### 2. First value

Los usuarios completan su primera sesión.

### 3. Mistake loop

Los usuarios vuelven a practicar errores.

### 4. Retention

Los usuarios regresan varios días después.

### 5. Learning

Los usuarios mejoran en sus áreas débiles.

### 6. Demand

Usuarios de LinkedIn llegan al producto y completan práctica.

La señal más importante:

> **Do users come back specifically to practice what they got wrong?**

------------------------------------------------------------------------

# 39. Development Order

No empezar programando todas las features.

## Step 1 --- Content

Convertir:

``` text
Google notes
Blend notes
SQL / ML notes
```

en preguntas estructuradas.

Objetivo:

> First 50 Data Engineering questions.

## Step 2 --- Learning loop

Construir:

``` text
Question
→ Answer
→ Explanation
→ Mistake
→ Review
```

## Step 3 --- Diagnostic

Agregar:

> 5-question diagnostic

## Step 4 --- Practice My Mistakes

Convertir los errores en sesiones adaptativas.

## Step 5 --- Progress

Agregar:

-   weak areas;
-   readiness;
-   review queue.

## Step 6 --- Open answers

Agregar:

-   flashcards;
-   short answer;
-   interview mode.

## Step 7 --- Mock interview

Solo cuando el contenido y learning loop estén funcionando.

## Step 8 --- Monetization

Validar willingness to pay.

## Step 9 --- Expansion

Recién entonces agregar otros roles.

------------------------------------------------------------------------

# 40. Final Product Definition

## Working name

**Data Interview Gym**

## Positioning

> **Your interview gym for Data.**

## One-line description

> A practice platform that helps Data professionals prepare for
> technical interviews through adaptive questions, mistake repetition
> and realistic interview simulations.

## Core promise

> **Don't study interviews. Practice them.**

## Core experience

``` text
Open app
   ↓
See what needs practice
   ↓
5–10 minute session
   ↓
Answer
   ↓
Learn
   ↓
Repeat mistakes
   ↓
Track progress
   ↓
Simulate interview
   ↓
Become interview-ready
```

## Product moat

``` text
High-quality interview content
           +
Adaptive learning
           +
Mistake repetition
           +
Realistic interview practice
```

## Final principle

> **Easy to start. Fast to practice. Hard to forget.**
