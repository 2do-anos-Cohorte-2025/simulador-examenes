import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RespuestaService {
  private apiUrl = 'http://localhost:8000/api/'; 

  constructor(private http: HttpClient) {}

 
  
  guardarRespuesta(data: {intentoId: number;preguntaId: number;opcionId: number | null;respuestaText: string | null;}): Observable<any> {
  return this.http.post(`${this.apiUrl}respuestas/`, {
    intento: data.intentoId,  
    pregunta: data.preguntaId,  
    opcion_seleccionada: data.opcionId,  
    respuesta_texto: data.respuestaText === "null" ? null : data.respuestaText  
  });
}
  getRespuesta(intentoId: number, preguntaId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/respuestas/?intento_id=${intentoId}&pregunta_id=${preguntaId}`);
  }
  getOpcion(opcionId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}opciones/${opcionId}/`);
  }
}