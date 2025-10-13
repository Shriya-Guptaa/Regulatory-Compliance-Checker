# email_notifier.py - Compact Email Notification System with Tight Design

import yagmail
import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()


class EmailNotifier:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.notification_emails = self._get_notification_emails()

        if not self.email_user or not self.email_password:
            print("⚠️ Email credentials not configured. Email notifications disabled.")
            self.enabled = False
        else:
            self.enabled = True
            try:
                self.yag = yagmail.SMTP(self.email_user, self.email_password)
                print("✅ Email system initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize email system: {e}")
                self.enabled = False

    def _get_notification_emails(self):
        """Get notification email addresses from environment"""
        emails_str = os.getenv("NOTIFICATION_EMAILS", "")
        if emails_str:
            return [email.strip() for email in emails_str.split(",") if email.strip()]
        else:
            return ["admin@company.com", "compliance@company.com", "legal@company.com"]

    def _check_user_session(self):
        """Check if user is authenticated and NOT in temp session"""
        try:
            is_authenticated = st.session_state.get("authenticated", False)
            is_temp = st.session_state.get("temp_session", False)
            
            if not is_authenticated or is_temp:
                print("⚠️ Temporary or unauthenticated session - email blocked")
                return False
            
            return True
        except Exception as e:
            print(f"⚠️ Session check failed: {e}")
            return False

    def _get_user_info(self):
        """Get current user information from session"""
        try:
            user_name = st.session_state.get("user_name", "Unknown User")
            user_email = st.session_state.get("user_email", "unknown@email.com")
            return user_name, user_email
        except:
            return "Unknown User", "unknown@email.com"

    def generate_analysis_summary(self, analysis_results, contract_name):
        """Generate a compact, tightly-spaced HTML email"""
        if not analysis_results:
            return None

        # Check user session
        if not self._check_user_session():
            print("⚠️ Temp session detected — email generation skipped")
            return None

        df = pd.DataFrame(analysis_results)
        user_name, user_email = self._get_user_info()

        # Calculate statistics
        total_clauses = len(df)
        high_risk = len(df[df["risk_level"] == "High"])
        medium_risk = len(df[df["risk_level"] == "Medium"])
        low_risk = len(df[df["risk_level"] == "Low"])
        compliance_rate = (low_risk / total_clauses * 100) if total_clauses > 0 else 0

        # Determine overall risk status
        if high_risk > 0:
            status_color = "#ef4444"
            status_icon = "🚨"
            status_text = "HIGH RISK"
        elif medium_risk > total_clauses * 0.5:
            status_color = "#f59e0b"
            status_icon = "⚠️"
            status_text = "MODERATE"
        else:
            status_color = "#10b981"
            status_icon = "✅"
            status_text = "LOW RISK"

        # Build compact HTML email
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:15px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#f3f4f6;">
            <table width="100%" style="max-width:480px;margin:0 auto;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                
                <!-- Header -->
                <tr>
                    <td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:18px 15px;text-align:center;">
                        <div style="font-size:28px;margin-bottom:5px;">⚖️</div>
                        <h1 style="margin:0;color:#fff;font-size:18px;font-weight:700;letter-spacing:-0.3px;">Contract Analysis</h1>
                    </td>
                </tr>
                
                <!-- Status -->
                <tr>
                    <td style="padding:12px 15px;background:{status_color};text-align:center;">
                        <h2 style="margin:0;color:#fff;font-size:16px;font-weight:700;letter-spacing:0.5px;">{status_icon} {status_text}</h2>
                    </td>
                </tr>
                
                <!-- Content -->
                <tr>
                    <td style="padding:15px;">
                        
                        <!-- Info -->
                        <div style="background:#f9fafb;border-radius:6px 6px 0 0;padding:10px;margin:0;">
                            <table width="100%" cellpadding="3" cellspacing="0">
                                <tr>
                                    <td style="color:#6b7280;font-size:12px;width:35%;">Contract:</td>
                                    <td style="color:#111827;font-size:12px;font-weight:600;">{contract_name}</td>
                                </tr>
                                <tr>
                                    <td style="color:#6b7280;font-size:12px;">By:</td>
                                    <td style="color:#111827;font-size:12px;font-weight:600;">{user_name}</td>
                                </tr>
                                <tr>
                                    <td style="color:#6b7280;font-size:12px;">Date:</td>
                                    <td style="color:#111827;font-size:12px;font-weight:600;">{datetime.now().strftime('%b %d, %Y')}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <!-- Metrics -->
                        <table width="100%" cellpadding="0" cellspacing="0" style="margin:0;">
                            <tr>
                                <td width="25%" style="text-align:center;padding:10px 0;background:#3b82f6;">
                                    <div style="color:rgba(255,255,255,0.85);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Total</div>
                                    <div style="color:#fff;font-size:22px;font-weight:700;line-height:1;">{total_clauses}</div>
                                </td>
                                <td width="25%" style="text-align:center;padding:10px 0;background:#ef4444;">
                                    <div style="color:rgba(255,255,255,0.85);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">High</div>
                                    <div style="color:#fff;font-size:22px;font-weight:700;line-height:1;">{high_risk}</div>
                                </td>
                                <td width="25%" style="text-align:center;padding:10px 0;background:#f59e0b;">
                                    <div style="color:rgba(255,255,255,0.85);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Med</div>
                                    <div style="color:#fff;font-size:22px;font-weight:700;line-height:1;">{medium_risk}</div>
                                </td>
                                <td width="25%" style="text-align:center;padding:10px 0;background:#10b981;">
                                    <div style="color:rgba(255,255,255,0.85);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Low</div>
                                    <div style="color:#fff;font-size:22px;font-weight:700;line-height:1;">{low_risk}</div>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Compliance Bar -->
                        <div style="background:#f9fafb;padding:10px;margin:0;">
                            <div style="margin-bottom:6px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="color:#6b7280;font-size:11px;font-weight:600;">Compliance Rate</td>
                                        <td style="color:#111827;font-size:13px;font-weight:700;text-align:right;">{compliance_rate:.0f}%</td>
                                    </tr>
                                </table>
                            </div>
                            <div style="background:#e5e7eb;height:7px;border-radius:10px;overflow:hidden;">
                                <div style="background:linear-gradient(90deg,#10b981,#059669);height:100%;width:{compliance_rate}%;border-radius:10px;"></div>
                            </div>
                        </div>
                        
                        <!-- Note -->
                        <div style="background:#f9fafb;border-radius:0 0 6px 6px;padding:8px;text-align:center;margin:0;">
                            <p style="margin:0;color:#6b7280;font-size:11px;line-height:1.4;">
                                📊 View full analysis in your dashboard
                            </p>
                        </div>
                        
                    </td>
                </tr>
                
                <!-- Footer -->
                <tr>
                    <td style="background:#f9fafb;padding:10px;text-align:center;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#9ca3af;font-size:10px;line-height:1.3;">AI Compliance Dashboard<br>{datetime.now().strftime('%b %d, %Y')}</p>
                    </td>
                </tr>
                
            </table>
        </body>
        </html>
        """
        
        return html

    def send_analysis_notification(self, analysis_results, contract_name):
        """Send compact email notification only if user is logged in"""
        if not self.enabled:
            print("📧 Email notifications disabled - skipping send")
            return False

        if not self._check_user_session():
            print("⚠️ Temp session or unauthenticated - email blocked")
            return False

        try:
            summary_html = self.generate_analysis_summary(analysis_results, contract_name)
            if not summary_html:
                print("⚠️ Summary generation failed - user session invalid")
                return False

            high_risk = len([r for r in analysis_results if r["risk_level"] == "High"])
            medium_risk = len([r for r in analysis_results if r["risk_level"] == "Medium"])

            if high_risk > 0:
                subject = f"🚨 HIGH RISK: {contract_name}"
            elif medium_risk > 0:
                subject = f"⚠️ Review: {contract_name}"
            else:
                subject = f"✅ Complete: {contract_name}"

            self.yag.send(
                to=self.notification_emails,
                subject=subject,
                contents=[summary_html],
            )

            print(f"✅ Email sent to {len(self.notification_emails)} recipient(s)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

    def send_test_email(self):
        """Send compact test email"""
        if not self.enabled:
            return False, "Email system not configured"
        
        if not self._check_user_session():
            return False, "Temporary session - email blocked"

        try:
            user_name, user_email = self._get_user_info()
            
            content = f"""
            <!DOCTYPE html>
            <html>
            <body style="margin:0;padding:15px;font-family:Arial,sans-serif;background:#f3f4f6;">
                <table width="100%" style="max-width:380px;margin:0 auto;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="background:linear-gradient(135deg,#10b981,#059669);padding:20px;text-align:center;">
                            <div style="font-size:36px;margin-bottom:5px;">✅</div>
                            <h1 style="margin:0;color:#fff;font-size:17px;font-weight:700;">Test Successful</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:15px;">
                            <div style="background:#f9fafb;border-radius:6px;padding:10px;">
                                <table width="100%" cellpadding="3" cellspacing="0">
                                    <tr>
                                        <td style="color:#6b7280;font-size:11px;width:35%;">Sent By:</td>
                                        <td style="color:#111827;font-size:11px;font-weight:600;">{user_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="color:#6b7280;font-size:11px;">Email:</td>
                                        <td style="color:#667eea;font-size:11px;font-weight:600;">{user_email}</td>
                                    </tr>
                                    <tr>
                                        <td style="color:#6b7280;font-size:11px;">Time:</td>
                                        <td style="color:#111827;font-size:11px;font-weight:600;">{datetime.now().strftime('%b %d, %I:%M %p')}</td>
                                    </tr>
                                </table>
                            </div>
                            <div style="text-align:center;margin-top:12px;">
                                <span style="display:inline-block;background:#10b981;color:#fff;padding:6px 18px;border-radius:15px;font-weight:600;font-size:11px;">System OK</span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="background:#f9fafb;padding:10px;text-align:center;border-top:1px solid #e5e7eb;">
                            <p style="margin:0;color:#9ca3af;font-size:9px;">AI Compliance Dashboard</p>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            self.yag.send(
                to=self.notification_emails,
                subject="✅ Test Email",
                contents=[content]
            )
            
            return True, f"✅ Test sent to {len(self.notification_emails)} recipient(s)"
            
        except Exception as e:
            return False, f"❌ Failed: {e}"

    def get_notification_recipients(self):
        return self.notification_emails

    def is_enabled(self):
        return self.enabled


# Global instance
email_notifier = EmailNotifier()