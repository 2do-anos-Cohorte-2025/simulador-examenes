// src/app/services/intento.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class IntentoService {
  private apiUrl = 'http://localhost:8000/api/intentos/'; // URL de tu API de Django

  constructor(private http: HttpClient) { }

  iniciarIntento(examenId: number, usuarioId: number): Observable<any> {
    return this.http.post(this.apiUrl, {
      examen: examenId,
      usuario: usuarioId,
    });
  }
  getIntento(intentoId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}${intentoId}/`);
  }

  finalizarIntento({intentoId, fecha_fin, resultado}: { intentoId: number, fecha_fin: Date, resultado: number }): Observable<any> {
    return this.http.put(`${this.apiUrl}${intentoId}/`, { fecha_fin, resultado });
  }
}
