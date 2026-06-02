import { Component, NgModule } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './shared/header/header.component';
import { FooterComponent } from './shared/footer/footer.component';
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { InicioComponent } from './views/inicio/inicio.component';
import { ExamenVistaPreviaComponent } from './views/examen-vista-previa/examen-vista-previa.component';
import { ExamenIntentoComponent } from './views/examen-intento/examen-intento.component';
import { ReactiveFormsModule } from '@angular/forms';




@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HttpClientModule, ReactiveFormsModule, DashboardComponent, InicioComponent, HeaderComponent, ExamenVistaPreviaComponent, ExamenIntentoComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'proyecto';

}
