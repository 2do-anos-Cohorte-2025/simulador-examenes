import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RespuestaService {
  private apiUrl = 'http://localhost:8000/api/'; // URL de tu API de Django

  constructor(private http: HttpClient) {}

 
  guardarRespuesta(respuesta: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/respuestas/`, {intento: respuesta.intentoId, pregunta: respuesta.preguntaId, opcion_seleccionada: respuesta.opcionId, respuesta_texto: respuesta.respuestaText});
  }
  getRespuesta(intentoId: number, preguntaId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/respuestas/?intento_id=${intentoId}&pregunta_id=${preguntaId}`);
  }
  getOpcion(opcionId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}opciones/${opcionId}/`);
  }
}