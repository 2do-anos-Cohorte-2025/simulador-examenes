import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../service/AuthService/auth.service';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent implements OnInit {
  usuario: any = null;
  cargando: boolean = true;
  error: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.getPerfil().subscribe({
      next: (data) => {
        this.usuario = data;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudo cargar el perfil.';
        this.cargando = false;
      }
    });
  }
}