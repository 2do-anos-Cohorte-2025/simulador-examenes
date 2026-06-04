import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GestionSolicitudesService {

  private apiUrl = 'http://localhost:8000/api/solicitudes-profesor/';

  constructor(private http: HttpClient) {}

  obtenerSolicitudes() {
    return this.http.get<any[]>(this.apiUrl);
  }

  obtenerSolicitud(id: number) {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }
}
