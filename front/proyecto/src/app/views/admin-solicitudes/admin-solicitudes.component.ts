import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SolicitudProfesorService } from '../../service/solicitud-profesor.service';

@Component({
  selector: 'app-admin-solicitudes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-solicitudes.component.html',
  styleUrl: './admin-solicitudes.component.css'
})
export class AdminSolicitudesComponent implements OnInit {

  solicitudes: any[] = [];
  solicitudSeleccionada: any = null;

  filtro = 'pendiente';

  constructor(
    private solicitudService: SolicitudProfesorService
  ) {}

  ngOnInit() {
    this.cargarSolicitudes();
  }

  cargarSolicitudes() {
    this.solicitudService.obtenerSolicitudes(this.filtro)
      .subscribe((data: any) => {
        this.solicitudes = data;
      });
  }

  seleccionarSolicitud(solicitud: any) {
    this.solicitudSeleccionada = solicitud;
  }

  cambiarFiltro(estado: string) {
    this.filtro = estado;
    this.solicitudSeleccionada = null;
    this.cargarSolicitudes();
  }

  aprobar() {
    if (!this.solicitudSeleccionada) return;
    this.solicitudService
      .aprobarSolicitud(this.solicitudSeleccionada.id)
      .subscribe(() => {
        alert('Solicitud aprobada');
        this.cargarSolicitudes();
        this.solicitudSeleccionada = null;
      });
  }

  rechazar() {
    if (!this.solicitudSeleccionada) return;
    this.solicitudService
      .rechazarSolicitud(this.solicitudSeleccionada.id)
      .subscribe(() => {
        alert('Solicitud rechazada');
        this.cargarSolicitudes();
        this.solicitudSeleccionada = null;
      });
  }
}
