import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as classes from "./Header.module.scss";
import { getCookie } from "@/shared/lib/cookies/getCookie";
import { parseJwt } from "@/shared/lib/jwt/parseJwt";
import { File } from "lucide-react";

const Header = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState(null);
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [isExportOpen, setIsExportOpen] = useState(false);
    const [showNotification, setShowNotification] = useState(false);

    const API_URL = import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const token = getCookie("access_token");
        if (token) {
            const payload = parseJwt(token);
            if (payload && payload.email) {
                setEmail(payload.email);
            }
        }
    }, []);

    const handleLogout = async () => {
        try {
            const response = await fetch(`${API_URL}/core/auth/logout`, {
                method: "POST",
                credentials: "include",
            });

            if (response.ok) {
                navigate("/");
            }
        } catch (error) {
            console.error("Logout failed:", error);
        }
    };

    const handleExport = async () => {
        try {
            const response = await fetch(`${API_URL}/core/prompt/pdf`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    start_time: new Date(startTime).toISOString(),
                    end_time: new Date(endTime).toISOString(),
                    limit: 1
                })
            });

            if (response.status === 202) {
                setShowNotification(true);
                setTimeout(() => setShowNotification(false), 3000);
            } else {
                console.error("Export request failed with status:", response.status);
            }
        } catch (error) {
            console.error("Export failed:", error);
        }
    };

    return (
        <header className={classes.header}>
            <div className={classes.container}>
                <button className={classes.logoutButton} onClick={handleLogout}>
                    Log out
                </button>

                <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                    {email && <div className={classes.userInfo}>{email}</div>}

                    <button
                        className={classes.logoutButton}
                        onClick={() => setIsExportOpen(!isExportOpen)}
                    >
                        <File size={20} />
                    </button>
                </div>
            </div>

            {isExportOpen && (
                <div style={{
                    backgroundColor: "#1f1f1f",
                    padding: "16px",
                    marginTop: "12px",
                    borderRadius: "8px",
                    maxWidth: "1280px",
                    marginLeft: "auto",
                    marginRight: "auto",
                    display: "flex",
                    gap: "12px",
                    alignItems: "center"
                }}>
                    <div>
                        <span style={{ color: '#94a3b8', fontSize: '14px' }}>Start time</span>
                        <input
                            type="datetime-local"
                            value={startTime}
                            onChange={(e) => setStartTime(e.target.value)}
                            style={{ padding: "8px 8px", borderRadius: "6px", border: "1px solid #ccc" }}
                        />
                    </div>
                    <div>
                        <span style={{ color: '#94a3b8', fontSize: '14px' }}>End time</span>
                        <input
                            type="datetime-local"
                            value={endTime}
                            onChange={(e) => setEndTime(e.target.value)}
                            style={{ padding: "8px 8px", borderRadius: "6px", border: "1px solid #ccc" }}
                        />
                    </div>
                    <button className={classes.logoutButton} onClick={handleExport}>
                        Send
                    </button>
                </div>
            )}

            {showNotification && (
                <div style={{
                    position: "fixed",
                    top: "20px",
                    right: "20px",
                    backgroundColor: "#1e509f",
                    color: "white",
                    padding: "12px 20px",
                    borderRadius: "8px",
                    boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
                    zIndex: 1000,
                    fontWeight: "bold"
                }}>
                    PDF report sent. Check your email.
                </div>
            )}
        </header>
    );
};

export default Header;
