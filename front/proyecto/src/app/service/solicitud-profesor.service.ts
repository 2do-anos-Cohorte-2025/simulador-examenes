import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SolicitudProfesorService {

  private apiUrl = 'http://127.0.0.1:8000/api/solicitudes-profesor/';

  constructor(private http: HttpClient) {}

  crearSolicitud(formData: FormData) {
    return this.http.post(this.apiUrl, formData);
  }

  obtenerSolicitudes(estado?: string) {
    if (estado) {
      return this.http.get(`${this.apiUrl}?estado=${estado}`);
    }
    return this.http.get(this.apiUrl);
  }

  obtenerSolicitud(id: number) {
    return this.http.get(`${this.apiUrl}${id}/`);
  }

  aprobarSolicitud(id: number) {
    return this.http.post(`${this.apiUrl}${id}/aprobar/`, {});
  }

  rechazarSolicitud(id: number) {
    return this.http.post(`${this.apiUrl}${id}/rechazar/`, {});
  }
}
