import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AdminService {

  private apiurl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  private headers(): HttpHeaders {
    const token = localStorage.getItem('access_token') || '';
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  // ── Usuarios
  getUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiurl}/usuarios/`, { headers: this.headers() });
  }
  crearUsuario(data: any): Observable<any> {
    return this.http.post(`${this.apiurl}/usuarios/`, data, { headers: this.headers() });
  }
  editarUsuario(id: number, data: any): Observable<any> {
    return this.http.patch(`${this.apiurl}/usuarios/${id}/`, data, { headers: this.headers() });
  }
  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.apiurl}/usuarios/${id}/`, { headers: this.headers() });
  }

  // ── Exámenes
  getExamenes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiurl}/examenes/`, { headers: this.headers() });
  }
  crearExamen(data: any): Observable<any> {
    return this.http.post(`${this.apiurl}/examenes/`, data, { headers: this.headers() });
  }
  editarExamen(slug: string, data: any): Observable<any> {
    return this.http.patch(`${this.apiurl}/examenes/${slug}/`, data, { headers: this.headers() });
  }
  eliminarExamen(slug: string): Observable<any> {
    return this.http.delete(`${this.apiurl}/examenes/${slug}/`, { headers: this.headers() });
  }
}