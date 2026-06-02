import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UsuarioService {
  private apiUrl = 'http://localhost:8000/api/'; 

  constructor(private http: HttpClient) {}


  getUsuario(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}usuarios/${id}/`);
  }
  getProfesor(id:number): Observable<any> {
    return this.http.get(`${this.apiUrl}profesores/${id}/`);
  }
}