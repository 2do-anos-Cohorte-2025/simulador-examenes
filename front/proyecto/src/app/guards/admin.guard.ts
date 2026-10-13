import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../service/AuthService/auth.service';

// Solo usuarios con rol administrador
export const adminGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.estaLogueado()) {
    return router.createUrlTree(['/login']);
  }
  return auth.getUsuario()?.rol === 'administrador'
    ? true
    : router.createUrlTree(['/inicio']);
};
