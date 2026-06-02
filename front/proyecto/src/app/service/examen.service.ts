import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

  // Obtener un examen por slug
  getExamen(slug: string): Observable<any> {
    return this.http.get(`${this.apiUrl}${slug}/`);
  }

}
