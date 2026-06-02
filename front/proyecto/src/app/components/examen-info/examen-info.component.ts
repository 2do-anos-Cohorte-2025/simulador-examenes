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
  usuario: any;
  slug: string | null = null;
  intento: string | null = null;
  date: any;

  constructor(
    private ExamenService: ExamenService,
    private IntentoService: IntentoService,
    private UsuarioService: UsuarioService,
  ) {


    this.slug = window.location.pathname.split('/')[2]; // Obtener el slug de la URL
    console.log('Slug del examen:', this.slug);

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

    // Recibir el IddelUser (REALIZAR)
    this.UsuarioService.getUsuario(1).subscribe({
      next: (usuario) => {
        this.usuario = usuario;
      },
      error: (error) => {
        console.error('Error al cargar el usuario:', error);
      }
    });
    }

    iniciarIntento(): void {
      const usuarioId = this.usuario?.id || 0;
      const examenId = this.examen?.id;
      this.IntentoService.iniciarIntento(examenId, usuarioId).subscribe({
        next: (response) => {
          this.intento = response.id;
          window.location.href = `/examen/${this.slug}/intento/${this.intento}`;
          console.log('Intento iniciado:', response);
        }
          
        
      });
    }

}
