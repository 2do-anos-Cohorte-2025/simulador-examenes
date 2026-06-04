import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NivelService {

  private apiUrl = 'http://localhost:8000/api/niveles/';

  constructor(private http: HttpClient) {}

  getNiveles(): Observable<any> {
     console.log("Pidiendo nivel");
    return this.http.get(this.apiUrl);
  }
}