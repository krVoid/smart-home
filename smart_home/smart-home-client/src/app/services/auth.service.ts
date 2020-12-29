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
  
    logout() {
      return this.http.post<any>(`${this.apiUrl}/revoke_token/`, {
        'refreshToken': this.getRefreshToken()
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
        'refresh_token': this.getRefreshToken()
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
  
    private getRefreshToken() {
      return localStorage.getItem(this.REFRESH_TOKEN);
    }
  
    private storeToken(jwt: string) {
      localStorage.setItem(this.JWT_TOKEN, jwt);
    }
  
    private storeTokens(tokens: TokenDto) {
      localStorage.setItem(this.JWT_TOKEN, tokens.access_token);
      localStorage.setItem(this.REFRESH_TOKEN, tokens.refresh_token);
    }
  
    private removeTokens() {
      localStorage.removeItem(this.JWT_TOKEN);
      localStorage.removeItem(this.REFRESH_TOKEN);
    }
}