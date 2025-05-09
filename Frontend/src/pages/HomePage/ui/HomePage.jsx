import { LibraryContent } from "@/shared/ui/widgets/LibraryContent";
import { Header } from "@/shared/ui/widgets/Header";
import * as classes from "./HomePage.module.scss";

const HomePage = () => {
    return (
        <>
            <Header />
            <main className={classes.main}>
                <LibraryContent />
            </main>
        </>
    );
};

export default HomePage;