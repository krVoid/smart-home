import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { Dashboardomponent, LoginComponent } from './components';
import { AuthGuard } from './services';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'dashboard',
    component: Dashboardomponent,
    canActivate: [AuthGuard]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
