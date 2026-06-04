import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SolicitudProfesorService } from '../../service/solicitud-profesor.service';

@Component({
  selector: 'app-solicitud-profesor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './solicitud-profesor.component.html',
  styleUrls: ['./solicitud-profesor.component.css']
})
export class SolicitudProfesorComponent {

  formData = {
    nombre_completo: '',
    dni: '',
    pais: '',
    provincia: '',
    telefono: '',
    institucion: '',
    especialidad: '',

  };

  certificadoTitulo!: File;
  dniFrente!: File;
  dniDorso!: File;

  constructor(
    private solicitudService: SolicitudProfesorService
  ) {}

  onFileChange(event: any, tipo: string) {

  const archivo = event.target.files[0];

  if (!archivo) return;

  switch(tipo) {

    case 'titulo':
      this.certificadoTitulo = archivo;
      break;

    case 'frente':
      this.dniFrente = archivo;
      break;

    case 'dorso':
      this.dniDorso = archivo;
      break;
  }
}

  enviarSolicitud() {

    const datos = new FormData();

    datos.append('nombre_completo', this.formData.nombre_completo);
    datos.append('dni', this.formData.dni);
    datos.append('pais', this.formData.pais);
    datos.append('provincia', this.formData.provincia);
    datos.append('telefono', this.formData.telefono);
    datos.append('institucion', this.formData.institucion);
    datos.append('especialidad', this.formData.especialidad);

    datos.append('certificado_titulo', this.certificadoTitulo);
    datos.append('dni_frente', this.dniFrente);
    datos.append('dni_dorso', this.dniDorso);

    this.solicitudService.crearSolicitud(datos).subscribe({
      next: () => {
        alert('Solicitud enviada correctamente');
      },
      error: (error) => {
        console.error(error);
        alert('Error al enviar la solicitud');
    }
  });
  }
}
