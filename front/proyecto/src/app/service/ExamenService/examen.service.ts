import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Examen, IntentoExamen } from './examen.model';



@Injectable({
  providedIn: 'root'
})
export class ExamenService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getExamen(id: number): Observable<Examen> {
    return this.http.get<Examen>(`${this.apiUrl}/${id}`);
  }

  getIntentoExamen(idIntento: number): Observable<IntentoExamen> {
    return this.http.get<IntentoExamen>(`${this.apiUrl}/intento/${idIntento}`);
  }

  enviarRespuestas(idIntento: number, respuestas: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/intento/${idIntento}/respuestas`, { respuestas });
  }
}
