import { ErrorHandler, Injector, Injectable } from '@angular/core';

@Injectable()
export class UncaughtExceptionsHandler implements ErrorHandler {
  constructor(private injector: Injector) {}

    public handleError(error: any): void {
        if(!error) {
            return;
        }
        console.log(error)
        const errorMessage = error.message || error.Message || error.error ; 
        alert(errorMessage);  
    }
}