import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTableModule } from '@angular/material/table';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {
  AdminDashboardComponent,
  Dashboardomponent,
  DeviceDetailsComponent,
  LoginComponent,
  RegisterComponent,
} from './components';
import { TokenInterceptor } from './services/token.interceptor';
import { NavbarComponent, SidenavComponent } from './ui';
import { UncaughtExceptionsHandler } from './services/uncaught-exception-handler.service';
import { ServerErrorHandlerInterceptor } from './services/server-error-handler.interceptor';
import { MatSidenavModule } from '@angular/material/sidenav';
import { InputsGridComponent } from './components/add-device/inputs-grid.component';
import { OutputsGridComponent } from './components/add-device/outputs-grid.component';
import { OutputComponent } from './components/output/output.component';
import { AdvancedActionsComponent } from './components/advance-actions/actions.component';
import { InputComponent } from './components/input/input.component';
import { MatDialogModule } from '@angular/material/dialog';
import { NotificationModalComponent } from './components/input/notification/notification.component';
import { MatSelectModule } from '@angular/material/select';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    Dashboardomponent,
    NavbarComponent,
    RegisterComponent,
    DeviceDetailsComponent,
    AdminDashboardComponent,
    SidenavComponent,
    InputsGridComponent,
    AdvancedActionsComponent,
    OutputsGridComponent,
    OutputComponent,
    InputComponent,
    NotificationModalComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
    MatSlideToggleModule,
    FormsModule,
    MatSidenavModule,
    MatDialogModule,
    MatExpansionModule,
    MatSelectModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ServerErrorHandlerInterceptor,
      multi: true,
    },
    {
      provide: ErrorHandler,
      useClass: UncaughtExceptionsHandler,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true,
    },
  ],
  entryComponents: [NotificationModalComponent],
  bootstrap: [AppComponent],
})
export class AppModule {}

// dsn="https://d729d8feb52a43d084830e4a04d68e02@o498265.ingest.sentry.io/5575611",
