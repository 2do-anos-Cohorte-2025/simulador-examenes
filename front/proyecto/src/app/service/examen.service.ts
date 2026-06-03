import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ExamenService {
  private apiUrl = 'http://localhost:8000/api/examenes/'; 

  constructor(private http: HttpClient) {}

  getExamenes(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  getExamen(slug: string): Observable<any> {
    return this.http.get(`${this.apiUrl}${slug}/`);
  }

  getExamenesFiltrados(
    categoria?: string,
    nivel?: string,
    creador?: string
  ): Observable<any> {

    let params = new HttpParams();

    if (categoria) {
      params = params.set('categoria', categoria);
    }

    if (nivel) {
      params = params.set('nivel', nivel);
    }

    if (creador) {
      params = params.set('creador', creador);
    }

    return this.http.get(this.apiUrl, { params });
  }
}