import { Routes } from '@angular/router';
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { InicioComponent } from './views/inicio/inicio.component';
import { LoginComponent } from './views/login/login.component';
import { RegistroComponent } from './views/registro/registro.component';
import { QuienesSomosComponent } from './views/quienes-somos/quienes-somos.component';
import { ExamenComponent } from './views/examen/examen.component';
import { SolicitudProfesorComponent } from './views/solicitud-profesor/solicitud-profesor.component';
import { PerfilComponent } from './views/perfil/perfil.component';


export const routes: Routes = [
    { path: 'inicio', component: InicioComponent },
    { path: 'dashboard', component: DashboardComponent },
    { path: '', redirectTo: '/inicio', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'registro', component: RegistroComponent },
    { path: 'perfil', component: PerfilComponent },
    { path: '', redirectTo: '/inicio', pathMatch: 'full' },
    { path: 'quienes-somos', component: QuienesSomosComponent },
    { path: 'examen/:slug', component: ExamenComponent },
    { path: 'examen/:slug/intento/:id', component: ExamenComponent },
    { path: 'solicitud-profesor', component: SolicitudProfesorComponent },
];
