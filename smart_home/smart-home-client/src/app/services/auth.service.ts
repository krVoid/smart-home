import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { of, Observable } from 'rxjs';
import { catchError, mapTo, tap } from 'rxjs/operators';
import { TokenDto } from '../dto'


@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private readonly JWT_TOKEN = 'JWT_TOKEN';
    private readonly REFRESH_TOKEN = 'REFRESH_TOKEN';
    private readonly apiUrl = 'http://localhost:8000/auth';
    private loggedUser: string;

    constructor(private http: HttpClient) {}

    isAdmin() {
      return this.http.get<boolean>(`${this.apiUrl}/is_superuser/`)
    }
  
    login(user: { username: string, password: string }): Observable<boolean> {
      return this.http.post<any>(`${this.apiUrl}/token/`, user)
        .pipe(
          tap(tokens => this.doLoginUser(user.username, tokens)),
          mapTo(true),
          catchError(error => {
            alert(error.error);
            return of(false);
          }));
    }
  
    register(user: { username: string, password: string, email: string }): Observable<boolean> {
      return this.http.post<any>(`${this.apiUrl}/register/`, user)
        .pipe(
          tap(tokens => this.doLoginUser(user.username, tokens)),
          mapTo(true),
          catchError(error => {
            alert(error.error);
            return of(false);
          }));
    }
  
    logout() {
      const t = this.getToken()      
      return this.http.post<any>(`${this.apiUrl}/revoke_token/`, {
        'token': t
      }).pipe(
        tap(() => this.doLogoutUser()),
        mapTo(true),
        catchError(error => {
          alert(error.error);
          return of(false);
        }));
    }
  
    isLoggedIn() {
      return !!this.getToken();
    }
  
    refreshToken() {
      return this.http.post<any>(`${this.apiUrl}/refresh_token/`, {
        'token': this.getToken()
      }).pipe(tap((tokens: TokenDto) => {
        this.storeTokens(tokens);
      }));
    }
  
    getToken() {
      return localStorage.getItem(this.JWT_TOKEN);
    }
  
    private doLoginUser(username: string, tokens: TokenDto) {
      this.loggedUser = username;
      this.storeTokens(tokens);
    }
  
    private doLogoutUser() {
      this.loggedUser = null;
      this.removeTokens();
    }
  
    private storeTokens(tokens: TokenDto) {
      localStorage.setItem(this.JWT_TOKEN, tokens.access_token);
    }
  
    private removeTokens() {
      localStorage.removeItem(this.JWT_TOKEN);
    }


    public getUsers(){
      return this.http.get<any>(`${this.apiUrl}/users/`);
  }
}