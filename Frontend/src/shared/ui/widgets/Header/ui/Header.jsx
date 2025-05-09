import { useNavigate } from "react-router-dom";
import * as classes from "./Header.module.scss";
import { useUser } from "@/shared/lib/context/UserContext";

const Header = () => {
    const navigate = useNavigate();
    const { userEmail } = useUser();

    const handleLogout = async () => {
        try {
            const response = await fetch("/auth/logout", {
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

    return (
        <header className={classes.header}>
            <div className={classes.container}>
                <button 
                    className={classes.logoutButton}
                    onClick={handleLogout}
                >
                    Log out
                </button>
                <div className={classes.userInfo}>
                    {userEmail}
                </div>
            </div>
        </header>
    );
};

export default Header; 