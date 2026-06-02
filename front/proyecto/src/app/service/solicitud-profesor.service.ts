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
}
