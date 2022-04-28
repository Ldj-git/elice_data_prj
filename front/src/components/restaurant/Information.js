import React from "react";
import { useSelector } from "react-redux";
import Googlemap from "./Googlemap";
import GoogleReviews from "./GoogleReviews";
import styles from "../../css/restaurant/Information.module.css";
import {
  StarBorderRounded as StarIcon,
  LocalDiningRounded as FoodIcon,
  AttachMoneyRounded as MoneyIcon,
  LocationOnOutlined as LocationIcon,
  Call as CallIcon,
  Link as LinkIcon,
} from "@mui/icons-material";

function Information() {
  const { restaurantInfo } = useSelector((state) => state.restaurant);

  return (
    <div className={styles.container}>
      <span className={styles.title}>Information</span>
      <div className={styles.content}>
        <div className={styles.left}>
          <div className={styles.information_list}>
            <div className={styles.information}>
              <StarIcon />
              <span>{restaurantInfo.award}</span>
            </div>
            <div className={styles.information}>
              <FoodIcon />
              <span>{restaurantInfo.cuisine?.join(", ")}</span>
            </div>
            <div className={styles.information}>
              <MoneyIcon />
              {/* 환전을 어떻게 하지 */}
              <span>
                {restaurantInfo.minPrice === restaurantInfo.maxPrice
                  ? restaurantInfo.minPrice
                  : `${restaurantInfo.minPrice} - ${restaurantInfo.maxPrice}`}{" "}
                ({restaurantInfo.currency})
              </span>
            </div>
            <div className={styles.information}>
              <LocationIcon />
              <span>{restaurantInfo.address}</span>
            </div>
            <div className={styles.information}>
              <CallIcon />
              <span>{restaurantInfo.phoneNumber}</span>
            </div>
            <div className={styles.information}>
              <LinkIcon />
              <span>
                <a
                  target="_blank"
                  href={
                    restaurantInfo.websiteUrl
                      ? restaurantInfo.websiteUrl
                      : restaurantInfo.url
                  }
                  alt="website"
                  rel="noreferrer"
                >
                  Restaurant Website
                </a>
              </span>
            </div>
          </div>
          <div className={styles.map}>{/* <Googlemap /> */}</div>
        </div>
        <div className={styles.right}>
          <GoogleReviews />
        </div>
      </div>
    </div>
  );
}

export default Information;
