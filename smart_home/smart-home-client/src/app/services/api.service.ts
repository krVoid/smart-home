import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private readonly apiUrl = 'http://localhost:8000/api';
    private loggedUser: string;

    constructor(private http: HttpClient) {}
  
    public getDevices(): Observable<boolean> {
      return this.http.get<any>(`${this.apiUrl}/devicedevice/`);
    }
  

}