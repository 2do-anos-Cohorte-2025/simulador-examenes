import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PreguntaService {
  private apiUrl = 'http://localhost:8000/api/'; 

  constructor(private http: HttpClient) {}

  // Obtener todas las preguntas de un examen
  getPreguntas(examenId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}preguntas/?examen_id=${examenId}`);
  }
  getPregunta(preguntaId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}preguntas/${preguntaId}/`);
  }
  createPregunta(data:any): Observable<any>{
    return this.http.post(`${this.apiUrl}preguntas/`, data);
  }
  // Obtener todas las opciones de una pregunta
  getOpciones(preguntaId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}opciones/?pregunta_id=${preguntaId}`);
  }
  createOpcion(data:any): Observable<any>{
    return this.http.post(`${this.apiUrl}opciones/`, data);
  }
}