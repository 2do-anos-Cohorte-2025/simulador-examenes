import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private apiUrl = 'http://localhost:8000/api/auth';

    constructor(private http: HttpClient) { }

    login(email: string, password_hash: string): Observable<any> {
        return this.http.post(`${this.apiUrl}/login/`, { email, password_hash }).pipe(
            tap((res: any) => {
                localStorage.setItem('access_token', res.access);
                localStorage.setItem('refresh_token', res.refresh);
                localStorage.setItem('usuario', JSON.stringify(res.usuario));
            })
        );
    }

    registro(datos: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/registro/`, datos).pipe(
            tap((res: any) => {
                localStorage.setItem('access_token', res.access);
                localStorage.setItem('refresh_token', res.refresh);
                localStorage.setItem('usuario', JSON.stringify(res.usuario));
            })
        );
    }

    getPerfil(): Observable<any> {
        const token = localStorage.getItem('access_token');

        const headers = new HttpHeaders({
            Authorization: `Bearer ${token}`
        });
        return this.http.get(`${this.apiUrl}/perfil/`, { headers });
    }

    logout(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('usuario');
    }

    getUsuario(): any {
        const u = localStorage.getItem('usuario');
        return u ? JSON.parse(u) : null;
    }

    estaLogueado(): boolean {
        return !!localStorage.getItem('access_token');
    }
    esProfesor(): boolean {
    const usuario = this.getUsuario();
    return usuario?.rol === 'profesor';
    }
}