import os
import smtplib
from email.mime.text import MIMEText

REMITENTE = os.getenv("SMTP_EMAIL", "smartparkingsolutions0@gmail.com")
CLAVE = os.getenv("SMTP_APP_PASSWORD")


def _login_smtp(server: smtplib.SMTP_SSL):
    if not CLAVE:
        raise RuntimeError("Falta SMTP_APP_PASSWORD en las variables de entorno.")
    server.login(REMITENTE, CLAVE)


def enviar_codigo(correo: str, codigo: str) -> None:
    content = f"""
    <tr>
      <td style="padding:36px 40px;">
        <p style="font-size:16px;color:#333333;margin:0 0 12px;">{HTML_WAVE} ¡Hola!</p>
        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 28px;">
          Aquí está tu código de verificación para continuar con tu registro en <strong>SmartParking</strong>:
        </p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
          <tr>
            <td align="center" style="background:#f0f4ff;border:2px dashed #4a6cf7;border-radius:10px;padding:24px;">
              <p style="margin:0 0 6px;font-size:13px;color:#888;letter-spacing:2px;text-transform:uppercase;">Código de verificación</p>
              <p style="margin:0;font-size:38px;font-weight:bold;color:#1a1a2e;letter-spacing:8px;">{HTML_LOCK} {codigo}</p>
            </td>
          </tr>
        </table>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:20px;">
          <tr>
            <td style="background:#fff8e1;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:14px 16px;">
              <p style="margin:0;font-size:14px;color:#92610a;">{HTML_CLOCK} <strong>Este código expira en 10 minutos.</strong> Ingrésalo antes de que venza.</p>
            </td>
          </tr>
        </table>

        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="background:#f9f9f9;border-left:4px solid #cccccc;border-radius:0 8px 8px 0;padding:14px 16px;">
              <p style="margin:0;font-size:13px;color:#888888;">{HTML_WARNING} ¿No solicitaste este registro? Puedes ignorar este correo con total tranquilidad.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    """
    _send_email(
        correo,
        f"{EMOJI_PARKING} SmartParking - Tu código de verificación",
        _email_shell(content),
    )


def enviar_aviso_empresa(correo: str) -> None:
    content = f"""
    <tr>
      <td style="padding:36px 40px;">
        <p style="font-size:16px;color:#333333;margin:0 0 12px;">{HTML_WAVE} ¡Hola!</p>
        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 28px;">
          Recibimos correctamente tu solicitud para crear una <strong>cuenta empresarial</strong> en nuestra plataforma. {HTML_PARTY}
        </p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
          <tr>
            <td align="center" style="background:#fffbeb;border:1px solid #f59e0b;border-radius:10px;padding:20px;">
              <p style="margin:0 0 6px;font-size:12px;color:#92610a;letter-spacing:2px;text-transform:uppercase;">Estado de tu solicitud</p>
              <p style="margin:0;font-size:22px;font-weight:bold;color:#b45309;">{HTML_SYNC} EN EVALUACIÓN</p>
            </td>
          </tr>
        </table>

        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 16px;">
          Nuestro equipo revisará la información proporcionada y te notificaremos con una respuesta en un plazo máximo de:
        </p>
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px;">
          <tr>
            <td align="center" style="background:#f0f4ff;border-radius:8px;padding:16px;">
              <p style="margin:0;font-size:20px;font-weight:bold;color:#1a1a2e;">{HTML_HOURGLASS} 24 horas</p>
            </td>
          </tr>
        </table>

        <p style="font-size:14px;color:#777777;margin:0;">
          Gracias por tu paciencia y por querer formar parte de nuestra red de socios. {HTML_HANDSHAKE}
        </p>
      </td>
    </tr>
    """
    _send_email(
        correo,
        f"{EMOJI_PARKING} SmartParking - Solicitud recibida y en evaluación",
        _email_shell(content),
    )


def enviar_confirmacion_aprobacion(correo: str) -> None:
    portal_url = _portal_url()
    content = f"""
    <tr>
      <td style="padding:36px 40px;">
        <p style="font-size:22px;color:#333333;font-weight:bold;margin:0 0 8px;">{HTML_PARTY} ¡Excelentes noticias!</p>
        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 28px;">
          Tu solicitud empresarial ha sido revisada y tenemos una actualización para ti.
        </p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
          <tr>
            <td align="center" style="background:#f0fdf4;border:1px solid #22c55e;border-radius:10px;padding:20px;">
              <p style="margin:0 0 6px;font-size:12px;color:#166534;letter-spacing:2px;text-transform:uppercase;">Estado de tu solicitud</p>
              <p style="margin:0;font-size:22px;font-weight:bold;color:#15803d;">{HTML_CHECK} APROBADA</p>
            </td>
          </tr>
        </table>

        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 20px;">
          Tu cuenta empresarial ha sido <strong>verificada y activada</strong>. Ya puedes ingresar al portal con tu correo corporativo y contraseña. {HTML_KEY}
        </p>

        <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8faff;border-radius:10px;padding:20px;margin-bottom:28px;">
          <tr>
            <td>
              <p style="margin:0 0 12px;font-size:13px;color:#888;letter-spacing:1px;text-transform:uppercase;">Desde el portal podrás:</p>
              <p style="margin:0 0 8px;font-size:14px;color:#444;">{HTML_PIN} Configurar tu estacionamiento</p>
              <p style="margin:0 0 8px;font-size:14px;color:#444;">{HTML_BUILDING} Registrar niveles y divisiones</p>
              <p style="margin:0 0 8px;font-size:14px;color:#444;">{HTML_PARKING} Gestionar tus espacios</p>
              <p style="margin:0;font-size:14px;color:#444;">{HTML_CHART} Monitorear tu operación en tiempo real</p>
            </td>
          </tr>
        </table>

        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center">
              <a href="{portal_url}" style="display:inline-block;background:#1a1a2e;color:#ffffff;text-decoration:none;font-size:15px;font-weight:bold;padding:14px 36px;border-radius:8px;">
                {HTML_ROCKET} Ir al portal
              </a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    """
    _send_email(
        correo,
        f"{EMOJI_PARKING} SmartParking - Tu solicitud fue aprobada {EMOJI_CHECK}",
        _email_shell(content, f"{HTML_CONFETTI} ¡Bienvenido a la familia SmartParking!"),
    )


def enviar_rechazo_empresa(correo: str) -> None:
    content = f"""
    <tr>
      <td style="padding:36px 40px;">
        <p style="font-size:16px;color:#333333;margin:0 0 12px;">{HTML_WAVE} ¡Hola!</p>
        <p style="font-size:15px;color:#555555;line-height:1.6;margin:0 0 28px;">
          Revisamos cuidadosamente tu solicitud empresarial y lamentamos informarte que no pudo ser aprobada en esta ocasión.
        </p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
          <tr>
            <td align="center" style="background:#fef2f2;border:1px solid #f87171;border-radius:10px;padding:20px;">
              <p style="margin:0 0 6px;font-size:12px;color:#991b1b;letter-spacing:2px;text-transform:uppercase;">Estado de tu solicitud</p>
              <p style="margin:0;font-size:22px;font-weight:bold;color:#dc2626;">{HTML_CROSS} NO APROBADA</p>
            </td>
          </tr>
        </table>

        <table width="100%" cellpadding="0" cellspacing="0" style="background:#fafafa;border-radius:10px;padding:20px;margin-bottom:24px;">
          <tr>
            <td>
              <p style="margin:0 0 12px;font-size:13px;color:#888;letter-spacing:1px;text-transform:uppercase;">Esto puede ocurrir cuando:</p>
              <p style="margin:0 0 8px;font-size:14px;color:#555;">{HTML_DOC} La información enviada está incompleta</p>
              <p style="margin:0 0 8px;font-size:14px;color:#555;">{HTML_SEARCH} Los datos no superaron la validación</p>
              <p style="margin:0;font-size:14px;color:#555;">{HTML_CLIP} Falta documentación requerida</p>
            </td>
          </tr>
        </table>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:20px;">
          <tr>
            <td style="background:#eff6ff;border-left:4px solid #3b82f6;border-radius:0 8px 8px 0;padding:16px;">
              <p style="margin:0 0 6px;font-size:14px;color:#1e40af;font-weight:bold;">¿Crees que es un error?</p>
              <p style="margin:0 0 4px;font-size:13px;color:#3b5998;">{HTML_CHAT} soporte@smartparking.com</p>
              <p style="margin:0;font-size:13px;color:#555555;">{HTML_SYNC} Puedes volver a enviar tu solicitud con datos actualizados.</p>
            </td>
          </tr>
        </table>

        <p style="font-size:14px;color:#777777;margin:0;">
          Agradecemos tu interés en SmartParking y esperamos poder trabajar contigo próximamente. {HTML_RAISED}
        </p>
      </td>
    </tr>
    """
    _send_email(
        correo,
        f"{EMOJI_PARKING} SmartParking - Actualización sobre tu solicitud",
        _email_shell(content),
    )
