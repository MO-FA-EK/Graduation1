import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';
import { NgxStripeModule } from 'ngx-stripe';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    
    importProvidersFrom(NgxStripeModule.forRoot('pk_test_51SgB6a1hQYy14ilucp6IZek1k8gYBNCNyFOErJZovenNIB1R8frpVCDS7ogcMlTif6d6Z5MHSPpozF2d9ZjiD9dH009aBufCeh'))
  ]
};