import { Component } from '@angular/core';
import { ExamenInfoComponent } from '../../components/examen-info/examen-info.component';

@Component({
  selector: 'app-examen-vista-previa',
  standalone: true,
  imports: [ExamenInfoComponent],
  templateUrl: './examen-vista-previa.component.html',
  styleUrl: './examen-vista-previa.component.css'
})
export class ExamenVistaPreviaComponent {

}
