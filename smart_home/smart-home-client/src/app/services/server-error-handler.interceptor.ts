import { Injectable, Injector } from '@angular/core';
import {
  HttpInterceptor,
  HttpHandler,
  HttpEvent,
  HttpRequest,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, NEVER, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

@Injectable()
export class ServerErrorHandlerInterceptor implements HttpInterceptor {
  constructor(private injector: Injector) {}

  public intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.error instanceof ErrorEvent) {
          return throwError(error);
        }
        // alert(JSON.stringify(error.error));
        return NEVER;
      })
    );
  }
}
