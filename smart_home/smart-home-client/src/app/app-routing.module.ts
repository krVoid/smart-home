import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {
  AdminDashboardComponent,
  Dashboardomponent,
  LoginComponent,
  RegisterComponent,
} from './components';
import { DeviceDetailsComponent } from './components/add-device/devide-details.component';
import { AdminGuard, AuthGuard } from './services';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'register',
    component: RegisterComponent,
  },
  {
    path: 'dashboard',
    component: Dashboardomponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'device/:id',
    component: DeviceDetailsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'device',
    component: DeviceDetailsComponent,
    canActivate: [AuthGuard],
  },

  {
    path: 'admin',
    component: AdminDashboardComponent,
    canActivate: [AuthGuard, AdminGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
