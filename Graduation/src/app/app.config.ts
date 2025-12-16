import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';
import { NgxStripeModule } from 'ngx-stripe';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),

    importProvidersFrom(NgxStripeModule.forRoot('pk_test_TYooMQauvdEDq54NiTphI7jx'))
  ]
};
