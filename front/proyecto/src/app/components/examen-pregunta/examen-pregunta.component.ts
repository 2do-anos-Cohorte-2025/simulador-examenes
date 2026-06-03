import { Component, OnDestroy, OnInit } from '@angular/core';
import { PreguntaService } from '../../service/pregunta.service';
import { ExamenService } from '../../service/examen.service';
import { IntentoService } from '../../service/intento.service';
import { UsuarioService } from '../../service/usuario.service';
import { ActivatedRoute } from '@angular/router';
import { RespuestaService } from '../../service/respuesta.service';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs/internal/observable/forkJoin';
import { map } from 'rxjs/internal/operators/map';

@Component({
  selector: 'app-examen-pregunta',
  standalone: true,
  imports: [DatePipe, FormsModule],
  templateUrl: './examen-pregunta.component.html',
  styleUrl: './examen-pregunta.component.css'
})
export class ExamenPreguntaComponent {
  examen: any = {};
  examenSlug: any = String;
  intentoSlug: any = Number;
  usuario: any = {};
  intento: any = null;
  date: any | null = null;
  preguntas: any[] = [];
  opciones: any[] = [];
  respuestas: any[] = [];
  total: any = 0;
  calculoTotal: number = 0;
  puntajesPorPregunta: { [key: number]: number } = {};
  tiempoRestante: number = 0;
  tiempoTotal: number = 0;
  temporizador: any;
  preguntaActual: number = 0;
  preguntaFinalizada: boolean = false;
  examenFinalizado: boolean = false;
  tiempoExpirado: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private ExamenService: ExamenService,
    private IntentoService: IntentoService,
    private UsuarioService: UsuarioService,
    private RespuestaService: RespuestaService,
    private PreguntaService: PreguntaService
  ) {
    this.examenSlug = window.location.pathname.split('/')[2];
    this.intentoSlug = window.location.pathname.split('/')[4];

    ExamenService.getExamen(this.examenSlug).subscribe({
      next: (examen) => {
        this.examen = examen;
        this.conseguirPreguntas(examen.id);
        this.date = new Date();
        this.tiempoTotal = examen.tiempo_limite * 60; // Tiempo en segundos
        this.tiempoRestante = this.tiempoTotal;
        this.iniciarTemporizador();

      },
      error: (error) => {
        console.error('Error al cargar el examen:', error);
      }
    });



  }


  conseguirPreguntas(examenId: number): void {
    this.PreguntaService.getPreguntas(this.examen.id).subscribe({
      next: (preguntas) => {
        this.preguntas = preguntas;
        this.respuestas = this.preguntas.map(pregunta => ({
          pregunta_id: pregunta.id,
          opcion_seleccionada_id: null,
          respuesta_texto: null
        }));
        if (this.preguntas.length > 0) {
          this.preguntaActual = 0;
          this.conseguirOpciones(this.preguntas[this.preguntaActual].id);
        }
      },
      error: (error) => {
        console.error('Error al cargar las preguntas:', error);
      }
    });
  }

  conseguirOpciones(preguntaId: number): void {
    this.PreguntaService.getOpciones(preguntaId).subscribe({
      next: (opciones) => {
        this.opciones = opciones;
      }
      ,
      error: (error) => {
      }
    });
  }

  iniciarTemporizador(): void {

    this.temporizador = setInterval(() => {
      this.tiempoRestante--;

      if (this.tiempoRestante <= 0) {
        this.tiempoExpirado = true;
        this.finalizarExamen();
        clearInterval(this.temporizador);
      }
    }, 1000);
  }

  finalizarExamen(): void {
    if (this.intentoSlug) {
      this.IntentoService.finalizarIntento({
        intentoId: this.intentoSlug,
        fecha_fin: new Date(),
        resultado: this.calculoTotal
      }).subscribe({
        next: (response) => {
          this.examenFinalizado = true;
          this.intento = response;
          clearInterval(this.temporizador);
        },
        error: (error) => {
          console.error('Error al finalizar el examen:', error);
        }
      });
    }
  }


  seleccionarOpcion(preguntaId: number, opcion: any): void {

    const respuesta = this.respuestas.find(
      r => r.pregunta_id === preguntaId
    );

    const pregunta = this.preguntas.find(
      p => p.id === preguntaId
    );

    if (!respuesta || !pregunta) return;

    respuesta.opcion_seleccionada_id = opcion.id;
    respuesta.respuesta_texto = null;

    this.puntajesPorPregunta[preguntaId] =
      opcion.es_correcta ? Number(pregunta.puntos) : 0;

    this.calculoTotal = Object.values(this.puntajesPorPregunta)
      .reduce((total, puntos) => Number(total) + Number(puntos), 0);



    this.guardarRespuesta({
      intento: Number(this.intentoSlug),
      pregunta: preguntaId,
      opcion_seleccionada: opcion.id,
      respuesta_texto: null
    });
  }

  responderTexto(preguntaId: number, texto: string): void {

    const respuesta = this.respuestas.find(
      r => r.pregunta_id === preguntaId
    );

    const pregunta = this.preguntas.find(
      p => p.id === preguntaId
    );

    if (!respuesta || !pregunta) return;

    respuesta.respuesta_texto = texto;
    respuesta.opcion_seleccionada_id = null;

    this.puntajesPorPregunta[preguntaId] = Number(pregunta.puntos);

    this.calculoTotal = Object.values(this.puntajesPorPregunta)
      .reduce((total, puntos) => Number(total) + Number(puntos), 0);


    this.guardarRespuesta({
      intento: Number(this.intentoSlug),
      pregunta: preguntaId,
      opcion_seleccionada: null,
      respuesta_texto: texto
    });
  }

  siguientePregunta(): void {
    if (!this.respuestas[this.preguntaActual]?.opcion_seleccionada_id && !this.respuestas[this.preguntaActual]?.respuesta_texto) {
      alert('Por favor, responde la pregunta antes de continuar.');
      return;
    }
    else if (this.preguntaActual < this.preguntas.length - 1) {
      this.preguntaActual++;
      if (this.preguntas.length > 0 && this.preguntas[this.preguntaActual]?.id) {
        this.conseguirOpciones(this.preguntas[this.preguntaActual].id);
      } else {
        console.warn('Pregunta actual no disponible para cargar opciones');
      }

    } else {
      this.finalizarExamen();
      this.preguntaFinalizada = true;
    }
  }

  anteriorPregunta(): void {
    if (this.preguntaActual > 0) {
      this.preguntaActual--;
      this.conseguirOpciones(this.preguntas[this.preguntaActual].id);
    }
  }

  guardarRespuesta(data: { intento: number; pregunta: number; opcion_seleccionada: number | null; respuesta_texto: string | null; }): void {
    const respuesta = this.respuestas.find(r => r.pregunta_id === data.pregunta);
    if (respuesta && this.intentoSlug) {
      this.RespuestaService.guardarRespuesta({
        intentoId: data.intento,
        preguntaId: data.pregunta,
        opcionId: data.opcion_seleccionada,
        respuestaText: data.respuesta_texto
      }).subscribe({
        next: (response) => {
          console.log('Respuesta guardada:', response);
        },
        error: (error) => {
          console.error('Error al guardar la respuesta:', error);
        }
      });
    }
  }
}