import { Routes } from '@angular/router';
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { InicioComponent } from './views/inicio/inicio.component';
import { LoginComponent } from './views/login/login.component';
import { RegistroComponent } from './views/registro/registro.component';
import { QuienesSomosComponent } from './views/quienes-somos/quienes-somos.component';
import { ExamenVistaPreviaComponent } from './views/examen-vista-previa/examen-vista-previa.component';
import { ExamenIntentoComponent } from './views/examen-intento/examen-intento.component';
import { SolicitudProfesorComponent } from './views/solicitud-profesor/solicitud-profesor.component';


export const routes: Routes = [
    { path: 'inicio', component: InicioComponent },
    { path: 'dashboard', component: DashboardComponent },
    { path: 'login', component: LoginComponent },
    { path: 'registro', component: RegistroComponent },
    { path: 'quienes-somos', component: QuienesSomosComponent },
    { path: 'examen/:slug', component: ExamenVistaPreviaComponent },
    { path: 'examen/:slug/intento/:id', component: ExamenIntentoComponent },
    { path: '', redirectTo: '/inicio', pathMatch: 'full' },
    { path: 'solicitud-profesor', component: SolicitudProfesorComponent },
];
