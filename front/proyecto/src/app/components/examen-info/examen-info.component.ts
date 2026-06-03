import { Component } from '@angular/core';
import { ExamenService } from '../../service/examen.service';
import { IntentoService } from '../../service/intento.service';
import { UsuarioService } from '../../service/usuario.service';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-examen-info',
  standalone: true,
  imports: [DatePipe, RouterLink],
  templateUrl: './examen-info.component.html',
  styleUrl: './examen-info.component.css'
})
export class ExamenInfoComponent {
  examen: any;
  token: any = String;
  usuario: any = {};
  slug: string | null = null;
  intento: string | null = null;
  date: any;

  constructor(
    private ExamenService: ExamenService,
    private IntentoService: IntentoService,
    private UsuarioService: UsuarioService,
  ) {


    this.slug = window.location.pathname.split('/')[2]; //el slug funciona como lockupfield de examen

    this.examen = ExamenService.getExamen(this.slug!).subscribe({
      next: (examen) => {
        console.log(examen);
        this.date = new Date();
        this.examen = examen;
      },
      error: (error) => {
        console.error('Error al cargar el examen:', error);
      }
    });

    this.token = localStorage.getItem("access_token");
    if (this.token) {
      const usuarioString = localStorage.getItem("usuario");
      this.usuario = usuarioString ? JSON.parse(usuarioString) : null;
    }

    // Si el usuario es profesor conseguir la info de solicitud profesor

  }

  iniciarIntento(): void {
    const examenId = this.examen?.id;
    const usuarioId = this.usuario?.id;


    const data = {
      examen: examenId,
      usuario: usuarioId, 
    };


    console.log("data enviada:", data, "usuario", usuarioId)
    this.IntentoService.iniciarIntento(data).subscribe({
      next: (response) => {
        this.intento = response.id;
        window.location.href = `/examen/${this.slug}/intento/${this.intento}`;
        console.log('Intento iniciado:', response);
      }
    });


  }

}
